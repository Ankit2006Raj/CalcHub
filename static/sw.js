// Service Worker for PWA
const CACHE_NAME = 'calchub-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/css/animations.css',
    '/static/css/command-palette.css',
    '/static/css/ai-features.css',
    '/static/js/main.js',
    '/static/js/pdf-utils.js',
    '/static/js/ai-features.js',
    '/static/js/command-palette.js',
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
});

// Fetch from cache
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Cache hit - return response
                if (response) {
                    return response;
                }

                // Clone the request
                const fetchRequest = event.request.clone();

                return fetch(fetchRequest).then((response) => {
                    // Check if valid response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }

                    // Clone the response
                    const responseToCache = response.clone();

                    caches.open(CACHE_NAME)
                        .then((cache) => {
                            cache.put(event.request, responseToCache);
                        });

                    return response;
                });
            })
    );
});

// Update Service Worker
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];

    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
