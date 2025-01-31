# Verificação e instalação de pacotes
pacotes_necessarios <- c("sf", "spatstat.core", "spatstat.geom", "tibble")
pacotes_para_instalar <- pacotes_necessarios[!(pacotes_necessarios %in% installed.packages()[,"Package"])]

if(length(pacotes_para_instalar) > 0) {
  install.packages(pacotes_para_instalar)
}

# Carregamento das bibliotecas
library(sf)
library(tibble)
library(spatstat.core)
library(spatstat.geom)

# Leitura e transformação dos dados espaciais de roubos
roubos_sf <- read_sf("/home/ras/Documentos/mba/mba_dados-main/df_roubos_projetado.shp") %>% 
  st_transform(crs = 32723)

# Conversão do objeto sf para owin e ppp
groubos <- as.owin(st_bbox(roubos_sf))
coordinates <- st_coordinates(roubos_sf)

ppp_roubos <- ppp(x = coordinates[,1], y = coordinates[,2], window = groubos)

# Leitura e transformação da área de estudo
area_estudo <- read_sf("/home/ras/Documentos/mba/mba_dados-main/area_projetados.shp") %>% 
  st_transform(crs = 32723)

# Conversão da área de estudo para o objeto owin
area_estudo_gwin <- as.owin(st_bbox(area_estudo))

# Criação de um novo ppp considerando a área de estudo
roubos_ppp <- ppp(
  x = st_coordinates(roubos_sf)[,1], 
  y = st_coordinates(roubos_sf)[,2], 
  window = area_estudo_gwin
)

# Cálculo das funções de envelopes para análise espacial
funcao_G <- envelope(roubos_ppp, Gest, nsim = 1000, verbose = TRUE)
funcao_K <- envelope(roubos_ppp, Kest, nsim = 1000, verbose = TRUE)
funcao_F <- envelope(roubos_ppp, Fest, nsim = 1000, verbose = TRUE)

# Plotagem das funções para visualização
plot(funcao_G, main = "Função G - Vizinho Mais Próximo")
plot(funcao_K, main = "Função K de Ripley")
plot(funcao_F, main = "Função F - Espaços Vazios")



