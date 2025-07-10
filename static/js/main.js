document.addEventListener('DOMContentLoaded', () => {
    // Visi filtru elementi
    const keywordFilter = document.getElementById('keyword-filter');
    const categoryFilter = document.getElementById('category-filter');
    const minPriceFilter = document.getElementById('min-price-filter');
    const maxPriceFilter = document.getElementById('max-price-filter');
    const adsGrid = document.getElementById('ads-grid');

    // Funkcija, kas ielādē un attēlo sludinājumus
    async function fetchAndDisplayAds() {
        // 1. Nolasa filtru vērtības
        const keyword = keywordFilter.value;
        const category = categoryFilter.value;
        const minPrice = minPriceFilter.value;
        const maxPrice = maxPriceFilter.value;

        // 2. Izveido URL ar filtru parametriem
        let url = `/api/ads?`;
        if (keyword) url += `&keyword=${keyword}`;
        if (category) url += `&category=${category}`;
        if (minPrice) url += `&min_price=${minPrice}`;
        if (maxPrice) url += `&max_price=${maxPrice}`;
        
        try {
            // 3. Nosūta pieprasījumu serverim
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP kļūda! status: ${response.status}`);
            }
            const ads = await response.json();

            // 4. Notīra vecos sludinājumus un attēlo jaunos
            adsGrid.innerHTML = ''; 

            if (ads.length === 0) {
                adsGrid.innerHTML = '<p>Nekas netika atrasts. Mēģiniet mainīt filtru kritērijus.</p>';
                return;
            }

            ads.forEach(ad => {
                const card = document.createElement('div');
                card.className = 'card';
                
                // Formatējam cenu, lai būtu ar diviem cipariem aiz komata
                const priceFormatted = ad.price ? `${ad.price.toFixed(2)} €` : 'Cena nav norādīta';

                card.innerHTML = `
                    <img src="${ad.image_url || 'static/images/default.png'}" alt="${ad.title}" />
                    <div>
                        <h3>${ad.title}</h3>
                        <p class="card-description">${ad.description.substring(0, 40)}...</p>
                        <div class="card-price">${priceFormatted}</div>
                    </div>
                `;
                adsGrid.appendChild(card);
            });

        } catch (error) {
            console.error("Neizdevās ielādēt sludinājumus:", error);
            adsGrid.innerHTML = '<p>Kļūda, ielādējot sludinājumus. Lūdzu, mēģiniet vēlāk.</p>';
        }
    }

    // Pievieno notikumu klausītājus visiem filtriem.
    // Tie izsauks `fetchAndDisplayAds` katru reizi, kad vērtība mainās.
    [keywordFilter, categoryFilter, minPriceFilter, maxPriceFilter].forEach(filter => {
        // 'input' notikums reaģē uzreiz, 'change' - kad noņem fokusu
        filter.addEventListener('input', fetchAndDisplayAds); 
    });

    // Sākotnējā sludinājumu ielāde, kad lapa atveras
    fetchAndDisplayAds();
});