// Linha 1: Declara uma constante que não será reatribuída.
const $ = (s, root = document) => root.querySelector(s);

// Linha 3: Declara uma constante que não será reatribuída.
const search = $('#destinationSearch');
// Linha 4: Declara uma constante que não será reatribuída.
const region = $('#destinationRegion');
// Linha 5: Declara uma constante que não será reatribuída.
const count = $('#destinationCount');
// Linha 6: Declara uma constante que não será reatribuída.
const cards = [...document.querySelectorAll('.destination-card')];
// Linha 7: Declara uma constante que não será reatribuída.
const csrf = () => $('input[name="csrf_token"]')?.value || document.querySelector('meta[name="csrf-token"]')?.content || '';

// Linha 9: Declara uma constante que não será reatribuída.
const normalize = value => String(value ?? '')
  // Linha 10: Executa a instrução JavaScript desta linha.
  .toLowerCase()
  // Linha 11: Executa a instrução JavaScript desta linha.
  .normalize('NFD')
  // Linha 12: Executa a instrução JavaScript desta linha.
  .replace(/[\u0300-\u036f]/g, '');

// Linha 14: Declara uma função reutilizável.
function filterDestinations() {
  // Linha 15: Declara uma constante que não será reatribuída.
  const query = normalize(search?.value);
  // Linha 16: Declara uma constante que não será reatribuída.
  const selectedRegion = region?.value || '';
  // Linha 17: Declara uma variável cujo valor pode ser alterado.
  let visible = 0;

  // Linha 19: Define uma função de seta para executar a lógica indicada.
  cards.forEach(card => {
    // Linha 20: Declara uma constante que não será reatribuída.
    const matches = (!query || normalize(card.dataset.search).includes(query))
      // Linha 21: Executa a instrução JavaScript desta linha.
      && (!selectedRegion || card.dataset.region === selectedRegion);

    // Linha 23: Executa a instrução JavaScript desta linha.
    card.hidden = !matches;
    // Linha 24: Verifica uma condição antes de executar a lógica seguinte.
    if (matches) visible++;
  // Linha 25: Executa a instrução JavaScript desta linha.
  });

  // Linha 27: Verifica uma condição antes de executar a lógica seguinte.
  if (count) count.textContent = `${visible} destino(s)`;
// Linha 28: Executa a instrução JavaScript desta linha.
}

// Linha 30: Executa a instrução JavaScript desta linha.
async function toggleFavorite(button) {
  // Linha 31: Declara uma constante que não será reatribuída.
  const response = await fetch('/api/favoritos/destino', {
    // Linha 32: Executa a instrução JavaScript desta linha.
    method: 'POST',
    // Linha 33: Executa a instrução JavaScript desta linha.
    headers: {
      // Linha 34: Executa a instrução JavaScript desta linha.
      'Content-Type': 'application/json',
      // Linha 35: Executa a instrução JavaScript desta linha.
      'X-CSRFToken': csrf()
    // Linha 36: Executa a instrução JavaScript desta linha.
    },
    // Linha 37: Executa a instrução JavaScript desta linha.
    body: JSON.stringify({
      // Linha 38: Executa a instrução JavaScript desta linha.
      cidade: button.dataset.city,
      // Linha 39: Executa a instrução JavaScript desta linha.
      pais: button.dataset.country,
      // Linha 40: Executa a instrução JavaScript desta linha.
      uf: button.dataset.uf
    // Linha 41: Executa a instrução JavaScript desta linha.
    })
  // Linha 42: Executa a instrução JavaScript desta linha.
  });

  // Linha 44: Declara uma constante que não será reatribuída.
  const data = await response.json();
  // Linha 45: Verifica uma condição antes de executar a lógica seguinte.
  if (!response.ok) throw new Error(data.error || 'Não foi possível atualizar o favorito.');

  // Linha 47: Declara uma constante que não será reatribuída.
  const favorited = Boolean(data.favorited);
  // Linha 48: Adiciona, remove ou verifica classes CSS de um elemento.
  button.classList.toggle('is-favorite', favorited);
  // Linha 49: Executa a instrução JavaScript desta linha.
  button.textContent = favorited ? '♥' : '♡';
  // Linha 50: Executa a instrução JavaScript desta linha.
  button.setAttribute('aria-pressed', String(favorited));
  // Linha 51: Executa a instrução JavaScript desta linha.
  button.setAttribute('aria-label', `${favorited ? 'Remover' : 'Favoritar'} ${button.dataset.city} ${favorited ? 'dos favoritos' : ''}`.trim());
  // Linha 52: Executa a instrução JavaScript desta linha.
  button.title = favorited ? 'Remover dos favoritos' : 'Favoritar destino';
// Linha 53: Executa a instrução JavaScript desta linha.
}

// Linha 55: Registra uma função para responder a um evento da interface.
search?.addEventListener('input', filterDestinations);
// Linha 56: Registra uma função para responder a um evento da interface.
region?.addEventListener('change', filterDestinations);

// Linha 58: Define uma função de seta para executar a lógica indicada.
document.querySelectorAll('.favorite-destination').forEach(button => {
  // Linha 59: Define uma função de seta para executar a lógica indicada.
  button.addEventListener('click', async () => {
    // Linha 60: Verifica uma condição antes de executar a lógica seguinte.
    if (button.disabled) return;
    // Linha 61: Executa a instrução JavaScript desta linha.
    button.disabled = true;

    // Linha 63: Executa a instrução JavaScript desta linha.
    try {
      // Linha 64: Executa a instrução JavaScript desta linha.
      await toggleFavorite(button);
    // Linha 65: Executa a instrução JavaScript desta linha.
    } catch (error) {
      // Linha 66: Executa a instrução JavaScript desta linha.
      alert(error.message);
    // Linha 67: Executa a instrução JavaScript desta linha.
    } finally {
      // Linha 68: Executa a instrução JavaScript desta linha.
      button.disabled = false;
    // Linha 69: Executa a instrução JavaScript desta linha.
    }
  // Linha 70: Executa a instrução JavaScript desta linha.
  });
// Linha 71: Executa a instrução JavaScript desta linha.
});

// Linha 73: Define uma função de seta para executar a lógica indicada.
document.querySelectorAll('.use-destination').forEach(button => {
  // Linha 74: Define uma função de seta para executar a lógica indicada.
  button.addEventListener('click', () => {
    // Linha 75: Executa a instrução JavaScript desta linha.
    location.href = '/dashboard?destino=' + encodeURIComponent(button.dataset.city);
  // Linha 76: Executa a instrução JavaScript desta linha.
  });
// Linha 77: Executa a instrução JavaScript desta linha.
});

// Linha 79: Executa a instrução JavaScript desta linha.
filterDestinations();
