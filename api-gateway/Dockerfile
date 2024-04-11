# Utilisez l'image officielle de Nginx
FROM nginx:alpine

# Supprimez la configuration par défaut de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiez la configuration personnalisée de Nginx dans le conteneur
COPY nginx.conf /etc/nginx/conf.d

# Lancez Nginx en mode foreground
CMD ["nginx", "-g", "daemon off;"]
