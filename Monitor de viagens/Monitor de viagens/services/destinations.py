# Linha 1: Cria ou atualiza uma variável com o valor calculado à direita.
DESTINATIONS = [
    # Linha 2: Executa a instrução Python desta linha.
    {"cidade":"São Paulo","pais":"Brasil","uf":"SP","regiao":"Brasil","descricao":"Gastronomia, cultura, negócios e vida urbana.","pontos":["Avenida Paulista","Parque Ibirapuera","MASP","Mercado Municipal"]},
    # Linha 3: Executa a instrução Python desta linha.
    {"cidade":"Rio de Janeiro","pais":"Brasil","uf":"RJ","regiao":"Brasil","descricao":"Praias, mirantes, cultura e grandes cartões-postais.","pontos":["Cristo Redentor","Pão de Açúcar","Copacabana","Jardim Botânico"]},
    # Linha 4: Executa a instrução Python desta linha.
    {"cidade":"Gramado","pais":"Brasil","uf":"RS","regiao":"Brasil","descricao":"Serra gaúcha, gastronomia e clima de montanha.","pontos":["Rua Coberta","Lago Negro","Mini Mundo","Snowland"]},
    # Linha 5: Executa a instrução Python desta linha.
    {"cidade":"João Pessoa","pais":"Brasil","uf":"PB","regiao":"Brasil","descricao":"Praias urbanas, piscinas naturais e centro histórico.","pontos":["Praia do Seixas","Piscinas do Seixas","Centro Histórico","Praia de Tambaú"]},
    # Linha 6: Executa a instrução Python desta linha.
    {"cidade":"Natal","pais":"Brasil","uf":"RN","regiao":"Brasil","descricao":"Dunas, praias e passeios de buggy.","pontos":["Ponta Negra","Morro do Careca","Genipabu","Forte dos Reis Magos"]},
    # Linha 7: Executa a instrução Python desta linha.
    {"cidade":"Fortaleza","pais":"Brasil","uf":"CE","regiao":"Brasil","descricao":"Litoral, gastronomia e vida noturna.","pontos":["Praia do Futuro","Mercado Central","Centro Dragão do Mar","Beira-Mar"]},
    # Linha 8: Executa a instrução Python desta linha.
    {"cidade":"Foz do Iguaçu","pais":"Brasil","uf":"PR","regiao":"Brasil","descricao":"Natureza e uma das maiores atrações de fronteira do país.","pontos":["Cataratas do Iguaçu","Parque das Aves","Marco das Três Fronteiras","Usina de Itaipu"]},
    # Linha 9: Executa a instrução Python desta linha.
    {"cidade":"Bonito","pais":"Brasil","uf":"MS","regiao":"Brasil","descricao":"Ecoturismo, rios cristalinos e cavernas.","pontos":["Gruta do Lago Azul","Rio da Prata","Aquário Natural","Estância Mimosa"]},
    # Linha 10: Executa a instrução Python desta linha.
    {"cidade":"Maragogi","pais":"Brasil","uf":"AL","regiao":"Brasil","descricao":"Piscinas naturais e praias do litoral alagoano.","pontos":["Galés de Maragogi","Praia de Antunes","Praia de Barra Grande","Caminho de Moisés"]},
    # Linha 11: Executa a instrução Python desta linha.
    {"cidade":"Maceió","pais":"Brasil","uf":"AL","regiao":"Brasil","descricao":"Praias urbanas, piscinas naturais e culinária alagoana.","pontos":["Pajuçara","Ponta Verde","Praia de Ipioca","Feirinha de Artesanato"]},
    # Linha 12: Executa a instrução Python desta linha.
    {"cidade":"Recife","pais":"Brasil","uf":"PE","regiao":"Brasil","descricao":"Praias, história, museus e gastronomia.","pontos":["Recife Antigo","Marco Zero","Instituto Ricardo Brennand","Praia de Boa Viagem"]},
    # Linha 13: Executa a instrução Python desta linha.
    {"cidade":"Salvador","pais":"Brasil","uf":"BA","regiao":"Brasil","descricao":"Patrimônio histórico, cultura afro-brasileira e litoral.","pontos":["Pelourinho","Elevador Lacerda","Farol da Barra","Igreja do Bonfim"]},
    # Linha 14: Executa a instrução Python desta linha.
    {"cidade":"Porto Seguro","pais":"Brasil","uf":"BA","regiao":"Brasil","descricao":"Praias, história e acesso a Arraial d'Ajuda e Trancoso.","pontos":["Passarela do Descobrimento","Cidade Histórica","Arraial d'Ajuda","Praia do Mundaí"]},
    # Linha 15: Executa a instrução Python desta linha.
    {"cidade":"Florianópolis","pais":"Brasil","uf":"SC","regiao":"Brasil","descricao":"Ilha com praias, trilhas e gastronomia.","pontos":["Lagoa da Conceição","Praia da Joaquina","Santo Antônio de Lisboa","Praia dos Ingleses"]},
    # Linha 16: Executa a instrução Python desta linha.
    {"cidade":"Curitiba","pais":"Brasil","uf":"PR","regiao":"Brasil","descricao":"Parques, arquitetura e gastronomia.","pontos":["Jardim Botânico","Museu Oscar Niemeyer","Ópera de Arame","Parque Tanguá"]},
    # Linha 17: Executa a instrução Python desta linha.
    {"cidade":"Belo Horizonte","pais":"Brasil","uf":"MG","regiao":"Brasil","descricao":"Gastronomia, arquitetura e acesso a Inhotim e cidades históricas.","pontos":["Praça da Liberdade","Mercado Central","Lagoa da Pampulha","Museu de Arte da Pampulha"]},
    # Linha 18: Executa a instrução Python desta linha.
    {"cidade":"Brasília","pais":"Brasil","uf":"DF","regiao":"Brasil","descricao":"Arquitetura modernista, monumentos e cultura cívica.","pontos":["Catedral Metropolitana","Congresso Nacional","Praça dos Três Poderes","Memorial JK"]},
    # Linha 19: Executa a instrução Python desta linha.
    {"cidade":"Manaus","pais":"Brasil","uf":"AM","regiao":"Brasil","descricao":"Amazônia, rios e patrimônio do ciclo da borracha.","pontos":["Teatro Amazonas","Encontro das Águas","Mercado Adolpho Lisboa","Museu da Amazônia"]},
    # Linha 20: Executa a instrução Python desta linha.
    {"cidade":"Vitória","pais":"Brasil","uf":"ES","regiao":"Brasil","descricao":"Ilhas, praias, gastronomia e centro histórico capixaba.","pontos":["Convento da Penha","Praia de Camburi","Ilha das Caieiras","Centro Histórico"]},
    # Linha 21: Executa a instrução Python desta linha.
    {"cidade":"Arraial do Cabo","pais":"Brasil","uf":"RJ","regiao":"Brasil","descricao":"Águas claras, praias e passeios de barco.","pontos":["Praia do Forno","Prainhas do Pontal do Atalaia","Praia Grande","Ilha do Farol"]},
    # Linha 22: Executa a instrução Python desta linha.
    {"cidade":"Búzios","pais":"Brasil","uf":"RJ","regiao":"Brasil","descricao":"Praias, gastronomia e vida noturna na Região dos Lagos.","pontos":["Rua das Pedras","Praia de João Fernandes","Praia da Ferradura","Orla Bardot"]},
    # Linha 23: Executa a instrução Python desta linha.
    {"cidade":"Campos do Jordão","pais":"Brasil","uf":"SP","regiao":"Brasil","descricao":"Montanha, arquitetura europeia e gastronomia.","pontos":["Vila Capivari","Morro do Elefante","Parque Amantikir","Horto Florestal"]},
    # Linha 24: Executa a instrução Python desta linha.
    {"cidade":"Jericoacoara","pais":"Brasil","uf":"CE","regiao":"Brasil","descricao":"Dunas, lagoas e pôr do sol no litoral cearense.","pontos":["Duna do Pôr do Sol","Lagoa do Paraíso","Pedra Furada","Lagoa Azul"]},
    # Linha 25: Executa a instrução Python desta linha.
    {"cidade":"Porto de Galinhas","pais":"Brasil","uf":"PE","regiao":"Brasil","descricao":"Piscinas naturais, praias e passeios de jangada.","pontos":["Piscinas Naturais","Praia de Muro Alto","Praia de Maracaípe","Pontal de Maracaípe"]},
    # Linha 26: Executa a instrução Python desta linha.
    {"cidade":"Fernando de Noronha","pais":"Brasil","uf":"PE","regiao":"Brasil","descricao":"Parque marinho, praias e mergulho.","pontos":["Baía do Sancho","Baía dos Porcos","Praia do Leão","Mirante dos Irmãos"]},
    # Linha 27: Executa a instrução Python desta linha.
    {"cidade":"Bangkok","pais":"Tailândia","uf":"","regiao":"Internacional","descricao":"Templos, mercados, gastronomia e vida urbana intensa.","pontos":["Grand Palace","Wat Arun","Wat Pho","Chatuchak Market"]},
    # Linha 28: Executa a instrução Python desta linha.
    {"cidade":"Hong Kong","pais":"Hong Kong","uf":"","regiao":"Internacional","descricao":"Arranha-céus, cultura cantonesa e grandes mirantes.","pontos":["Victoria Peak","Star Ferry","Tsim Sha Tsui","Temple Street Night Market"]},
    # Linha 29: Executa a instrução Python desta linha.
    {"cidade":"Londres","pais":"Reino Unido","uf":"","regiao":"Internacional","descricao":"Museus, palácios, parques e história.","pontos":["Tower of London","British Museum","London Eye","Buckingham Palace"]},
    # Linha 30: Executa a instrução Python desta linha.
    {"cidade":"Macau","pais":"Macau","uf":"","regiao":"Internacional","descricao":"Patrimônio luso-asiático, gastronomia e entretenimento.","pontos":["Ruínas de São Paulo","Senado","Templo de A-Má","Torre de Macau"]},
    # Linha 31: Executa a instrução Python desta linha.
    {"cidade":"Istambul","pais":"Turquia","uf":"","regiao":"Internacional","descricao":"História entre Europa e Ásia, mesquitas e bazares.","pontos":["Hagia Sophia","Mesquita Azul","Palácio de Topkapi","Grande Bazar"]},
    # Linha 32: Executa a instrução Python desta linha.
    {"cidade":"Dubai","pais":"Emirados Árabes Unidos","uf":"","regiao":"Internacional","descricao":"Arquitetura, compras, praias e experiências no deserto.","pontos":["Burj Khalifa","Dubai Mall","Palm Jumeirah","Dubai Marina"]},
    # Linha 33: Executa a instrução Python desta linha.
    {"cidade":"Meca","pais":"Arábia Saudita","uf":"","regiao":"Internacional","descricao":"Importante destino religioso e centro da peregrinação islâmica.","pontos":["Masjid al-Haram","Kaaba","Abraj Al Bait","Jabal al-Nour"]},
    # Linha 34: Executa a instrução Python desta linha.
    {"cidade":"Antalya","pais":"Turquia","uf":"","regiao":"Internacional","descricao":"Costa mediterrânea, praias e sítios históricos.","pontos":["Kaleiçi","Portão de Adriano","Düden Waterfalls","Konyaaltı Beach"]},
    # Linha 35: Executa a instrução Python desta linha.
    {"cidade":"Paris","pais":"França","uf":"","regiao":"Internacional","descricao":"Arte, gastronomia, arquitetura e grandes museus.","pontos":["Torre Eiffel","Museu do Louvre","Arco do Triunfo","Montmartre"]},
    # Linha 36: Executa a instrução Python desta linha.
    {"cidade":"Kuala Lumpur","pais":"Malásia","uf":"","regiao":"Internacional","descricao":"Arranha-céus, culinária multicultural e templos.","pontos":["Petronas Twin Towers","Batu Caves","Merdeka Square","Bukit Bintang"]},
    # Linha 37: Executa a instrução Python desta linha.
    {"cidade":"Barcelona","pais":"Espanha","uf":"","regiao":"Internacional","descricao":"Gaudí, praia, gastronomia e arquitetura modernista.","pontos":["Sagrada Família","Park Güell","Casa Batlló","La Rambla"]},
    # Linha 38: Executa a instrução Python desta linha.
    {"cidade":"Palma de Mallorca","pais":"Espanha","uf":"","regiao":"Internacional","descricao":"Praias, centro histórico e paisagens mediterrâneas.","pontos":["Catedral de Palma","Palácio de Almudaina","Bellver Castle","Playa de Palma"]},
    # Linha 39: Executa a instrução Python desta linha.
    {"cidade":"Madrid","pais":"Espanha","uf":"","regiao":"Internacional","descricao":"Museus, parques, gastronomia e vida noturna.","pontos":["Museu do Prado","Parque do Retiro","Palácio Real","Plaza Mayor"]},
    # Linha 40: Executa a instrução Python desta linha.
    {"cidade":"Roma","pais":"Itália","uf":"","regiao":"Internacional","descricao":"Arqueologia, arte, gastronomia e patrimônio religioso.","pontos":["Coliseu","Fontana di Trevi","Fórum Romano","Panteão"]},
    # Linha 41: Executa a instrução Python desta linha.
    {"cidade":"Lisboa","pais":"Portugal","uf":"","regiao":"Internacional","descricao":"História, miradouros, gastronomia e proximidade do litoral.","pontos":["Torre de Belém","Mosteiro dos Jerónimos","Castelo de São Jorge","Praça do Comércio"]},
    # Linha 42: Executa a instrução Python desta linha.
    {"cidade":"Nova York","pais":"Estados Unidos","uf":"","regiao":"Internacional","descricao":"Museus, parques, musicais e grandes bairros culturais.","pontos":["Central Park","Times Square","Estátua da Liberdade","Metropolitan Museum of Art"]},
    # Linha 43: Executa a instrução Python desta linha.
    {"cidade":"Orlando","pais":"Estados Unidos","uf":"","regiao":"Internacional","descricao":"Parques temáticos, compras e entretenimento.","pontos":["Walt Disney World","Universal Orlando Resort","SeaWorld Orlando","International Drive"]},
    # Linha 44: Executa a instrução Python desta linha.
    {"cidade":"Buenos Aires","pais":"Argentina","uf":"","regiao":"Internacional","descricao":"Arquitetura, tango, gastronomia e bairros históricos.","pontos":["Obelisco","Caminito","Recoleta","Puerto Madero"]},
    # Linha 45: Executa a instrução Python desta linha.
    {"cidade":"Santiago","pais":"Chile","uf":"","regiao":"Internacional","descricao":"Cordilheira, vinhos, museus e vida urbana.","pontos":["Cerro San Cristóbal","Plaza de Armas","Sky Costanera","Barrio Bellavista"]},
    # Linha 46: Executa a instrução Python desta linha.
    {"cidade":"Tóquio","pais":"Japão","uf":"","regiao":"Internacional","descricao":"Tecnologia, tradição, gastronomia e bairros vibrantes.","pontos":["Senso-ji","Shibuya Crossing","Tokyo Skytree","Meiji Jingu"]},
    # Linha 47: Executa a instrução Python desta linha.
    {"cidade":"Cancún","pais":"México","uf":"","regiao":"Internacional","descricao":"Caribe, praias e acesso à Riviera Maya.","pontos":["Zona Hoteleira","Isla Mujeres","Museu Maya","Playa Delfines"]},
    # Linha 48: Executa a instrução Python desta linha.
    {"cidade":"Cidade do Cabo","pais":"África do Sul","uf":"","regiao":"Internacional","descricao":"Montanhas, praias, vinhos e natureza.","pontos":["Table Mountain","V&A Waterfront","Boulders Beach","Kirstenbosch"]},
    # Linha 49: Executa a instrução Python desta linha.
    {"cidade":"Amsterdam","pais":"Países Baixos","uf":"","regiao":"Internacional","descricao":"Canais, museus, bicicletas e arquitetura histórica.","pontos":["Museu Van Gogh","Rijksmuseum","Casa de Anne Frank","Vondelpark"]},
    # Linha 50: Executa a instrução Python desta linha.
    {"cidade":"Cairo","pais":"Egito","uf":"","regiao":"Internacional","descricao":"Arqueologia, história e acesso às pirâmides.","pontos":["Pirâmides de Gizé","Grande Esfinge","Museu Egípcio","Khan el-Khalili"]},
    # Linha 51: Executa a instrução Python desta linha.
    {"cidade":"Seul","pais":"Coreia do Sul","uf":"","regiao":"Internacional","descricao":"Tecnologia, cultura pop, palácios e gastronomia.","pontos":["Palácio Gyeongbokgung","Bukchon Hanok Village","N Seoul Tower","Myeongdong"]},
# Linha 52: Executa a instrução Python desta linha.
]
