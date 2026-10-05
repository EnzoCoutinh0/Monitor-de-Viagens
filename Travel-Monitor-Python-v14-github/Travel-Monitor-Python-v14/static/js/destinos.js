const $ = (s, root = document) => root.querySelector(s);

const search = $('#destinationSearch');
const region = $('#destinationRegion');
const count = $('#destinationCount');
const cards = [...document.querySelectorAll('.destination-card')];
const csrf = () => $('input[name="csrf_token"]')?.value || document.querySelector('meta[name="csrf-token"]')?.content || '';

const normalize = value => String(value ?? '')
  .toLowerCase()
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '');

function filterDestinations() {
  const query = normalize(search?.value);
  const selectedRegion = region?.value || '';
  let visible = 0;

  cards.forEach(card => {
    const matches = (!query || normalize(card.dataset.search).includes(query))
      && (!selectedRegion || card.dataset.region === selectedRegion);

    card.hidden = !matches;
    if (matches) visible++;
  });

  if (count) count.textContent = `${visible} destino(s)`;
}

async function toggleFavorite(button) {
  const response = await fetch('/api/favoritos/destino', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf()
    },
    body: JSON.stringify({
      cidade: button.dataset.city,
      pais: button.dataset.country,
      uf: button.dataset.uf
    })
  });

  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Não foi possível atualizar o favorito.');

  const favorited = Boolean(data.favorited);
  button.classList.toggle('is-favorite', favorited);
  button.textContent = favorited ? '♥' : '♡';
  button.setAttribute('aria-pressed', String(favorited));
  button.setAttribute('aria-label', `${favorited ? 'Remover' : 'Favoritar'} ${button.dataset.city} ${favorited ? 'dos favoritos' : ''}`.trim());
  button.title = favorited ? 'Remover dos favoritos' : 'Favoritar destino';
}

search?.addEventListener('input', filterDestinations);
region?.addEventListener('change', filterDestinations);

document.querySelectorAll('.favorite-destination').forEach(button => {
  button.addEventListener('click', async () => {
    if (button.disabled) return;
    button.disabled = true;

    try {
      await toggleFavorite(button);
    } catch (error) {
      alert(error.message);
    } finally {
      button.disabled = false;
    }
  });
});

document.querySelectorAll('.use-destination').forEach(button => {
  button.addEventListener('click', () => {
    location.href = '/dashboard?destino=' + encodeURIComponent(button.dataset.city);
  });
});

filterDestinations();
