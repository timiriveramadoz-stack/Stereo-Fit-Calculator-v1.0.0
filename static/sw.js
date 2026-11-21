
const CACHE_NAME = "stereo-fit-v2";

const ARCHIVOS = [
    "/static/style.css",
    "/static/manifest.json",
    "/static/icon-192.png",
    "/static/icon-512.png"
];


// INSTALACIÓN

self.addEventListener("install", function (evento) {

    evento.waitUntil(

        caches.open(CACHE_NAME).then(function (cache) {
            return cache.addAll(ARCHIVOS);
        })

    );

    self.skipWaiting();

});


// ACTIVACIÓN

self.addEventListener("activate", function (evento) {

    evento.waitUntil(

        caches.keys().then(function (nombres) {

            return Promise.all(

                nombres
                    .filter(function (nombre) {
                        return nombre.startsWith("stereo-fit-") &&
                               nombre !== CACHE_NAME;
                    })
                    .map(function (nombre) {
                        return caches.delete(nombre);
                    })

            );

        }).then(function () {

            return self.clients.claim();

        })

    );

});


// SOLICITUDES

self.addEventListener("fetch", function (evento) {

    const solicitud = evento.request;

    // Ignorar solicitudes que no sean GET
    if (solicitud.method !== "GET") {
        return;
    }

    const url = new URL(solicitud.url);

    // Solo gestionar solicitudes del mismo origen
    if (url.origin !== self.location.origin) {
        return;
    }

    // ARCHIVOS ESTÁTICOS: caché primero

    if (url.pathname.startsWith("/static/")) {

        evento.respondWith(

            caches.match(solicitud).then(function (respuestaCache) {

                if (respuestaCache) {
                    return respuestaCache;
                }

                return fetch(solicitud).then(function (respuesta) {

                    if (respuesta.ok) {

                        const copia = respuesta.clone();

                        caches.open(CACHE_NAME).then(function (cache) {
                            cache.put(solicitud, copia);
                        });

                    }

                    return respuesta;

                });

            })

        );

    }

});
