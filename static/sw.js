// Service Worker for PWA with Offline API Fallbacks
const CACHE_NAME = 'calchub-v2';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/css/animations.css',
    '/static/css/command-palette.css',
    '/static/css/navbar.css',
    '/static/css/footer.css',
    '/static/js/main.js',
    '/static/js/charts.js',
    '/bmi',
    '/bmr',
    '/loan',
    '/calorie',
    '/age',
    '/gpa',
    '/grade',
    '/pregnancy',
    '/percentage',
    '/attendance',
    '/compound-interest',
    '/math'
];

// Install Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
    self.skipWaiting();
});

// Activate & Cleanup Old Caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Offline Calculator Logic
const offlineCalculators = {
    '/api/bmi': async (request) => {
        const data = await request.clone().json();
        const heightM = data.height / 100;
        const bmi = (data.weight / (heightM * heightM)).toFixed(1);
        let category, color;
        if (bmi < 18.5) { category = "Underweight"; color = "#3498db"; }
        else if (bmi < 25) { category = "Normal weight"; color = "#2ecc71"; }
        else if (bmi < 30) { category = "Overweight"; color = "#f39c12"; }
        else { category = "Obese"; color = "#e74c3c"; }
        return new Response(JSON.stringify({ bmi: parseFloat(bmi), category, color }), {
            headers: { 'Content-Type': 'application/json' }
        });
    },
    '/api/loan': async (request) => {
        const data = await request.clone().json();
        const p = data.amount;
        const r = data.rate / 12 / 100;
        const n = data.duration * 12;
        const emi = (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
        const totalAmount = emi * n;
        return new Response(JSON.stringify({
            emi: emi.toFixed(2),
            total_interest: (totalAmount - p).toFixed(2),
            total_amount: totalAmount.toFixed(2)
        }), { headers: { 'Content-Type': 'application/json' }});
    },
    '/api/percentage': async (request) => {
        const data = await request.clone().json();
        const value = eval(data.marks.replace(/[^0-9\+\-\*\/\(\)\.]/g, ''));
        return new Response(JSON.stringify({ percentage: value, grade: "Offline Mode", total: value }), {
            headers: { 'Content-Type': 'application/json' }
        });
    }
};

// Fetch Strategy: Network First, falling back to Cache, falling back to Offline Calculators
self.addEventListener('fetch', (event) => {
    // Handle API requests
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request).catch(async () => {
                const url = new URL(event.request.url);
                if (offlineCalculators[url.pathname] && event.request.method === 'POST') {
                    console.log('Serving offline calculator fallback for', url.pathname);
                    return await offlineCalculators[url.pathname](event.request);
                }
                return new Response(JSON.stringify({ error: "You are offline and this calculator requires an internet connection." }), {
                    status: 503, headers: { 'Content-Type': 'application/json' }
                });
            })
        );
        return;
    }

    // Handle static assets & HTML
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) return cachedResponse;
            return fetch(event.request).then((response) => {
                if (!response || response.status !== 200 || response.type !== 'basic') {
                    return response;
                }
                const responseToCache = response.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseToCache);
                });
                return response;
            }).catch(() => {
                // Return offline page or fallback if applicable
            });
        })
    );
});
