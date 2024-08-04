
# Projeto Q-learning:

## O que vai ser dado:

Para esse projeto, será disponibilizado:
> - um arquivo .exe que contém o jogo ([drive](https://drive.google.com/drive/folders/1zY6J2Zx63e0PIDa3wLt2zMoV0NKUCLcd?usp=sharing));
> - um projeto em python no GitHub que contém um arquivo chamado **connection.py** (i.e., a conexão com o servidor local do jogo) e um outro arquivo chamado **client.py**, que será onde vocês irão implementar o algoritmo de vocês.

## Objetivo do jogo:

Neste jogo controlamos o personagem Amongois, que terá que passar por diversas plataformas para chegar no seu objetivo final que é o bloco preto. Para isso ele pode fazer 3 movimentos, sendo eles, girar para a esquerda, girar para a direita e pular para a frente.

![enter image description here](https://lh7-us.googleusercontent.com/docsz/AD_4nXeovh0eE5bzdCaioLgln9Oa99VWrbJrPF8aiJwsyzbUwFi6pdPa_Fk8c1BKqa59qKA6O-0N6mSIPekaY7ID_9QoFWofSJfPNvqUXuBGWGjeXx35HaOGS3jAIna5ip0Jc925CRe8OtoSsYyaUf5TYcgXyW5Sscs0Nf-oeKszTarTufeguceGZQ?key=PZ_BjQO2n0pROWE1ICmcPA)

## Objetivo do projeto:

O objetivo do projeto é implementar o algoritmo Q-Learning para aprender o trajeto que deve ser tomado pelo Amongois no jogo.

## Como conectar o seu algoritmo ao jogo:

Para que haja uma comunicação entre o algoritmo e o jogo, vocês irão inicialmente importar o connection.py para o client.py (local onde vocês irão implementar o algoritmo). Para vocês iniciarem a conexão, devem chamar a função connect() que irá retornar o socket com a conexão. O connect() recebe a porta utilizada pelo executável como argumento.

Após realizada a conexão, a comunicação irá se dar pela função get_state_reward(). Essa função recebe a ação que deve ser feita pelo personagem e o socket recebido na função connect(), e terá como retorno, o estado atual e a recompensa.

### Exemplo:

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXetevH66fgG8S9oD38PNKbBrxBEXOkmsdot8WEDoDSoC1g4vkItSPStE_nRhrNWEzWEMvTt1vxyrqiBWKskt4SqEMktAAlpBAgGwsmLmYZFGdLkHdyOzhZQLVjDpXtQ1b-BoPGcUaU-JyNFZiDqXa1Rcn8KxQEcG-AYsVJyhCAal8kYBOFK-Q?key=PZ_BjQO2n0pROWE1ICmcPA)

## ![](https://lh7-us.googleusercontent.com/docsz/AD_4nXdf1OO2lzKpPornFvflR9ylpIy7KGCpDmMGT3R9PKmEefOVd9aC-m_yVqAf4_ISMao9aG24wHgpnm-KCP8gEq5fIiw7IzJQQ7PJLTsbYfJln8iJyhBUt6bjTmaHAzNbGvPD7gamdIpIX1crhK_CY7LaCC7cD7oiufriwd6VAuZ_TBSIV2TP?key=PZ_BjQO2n0pROWE1ICmcPA)

## Como é o formato das informações enviadas para o jogo:

A informação para cada ação é representada por uma string correspondente:
> "left" = Girar para a Esquerda
> 
> "right" = Girar para a Direita
> 
> "jump" = Pular para a Frente

## Como jogar

Você pode jogar manualmente ou você pode controlar o jogo da forma descrita acima.

### Jogando manualmente
É só utilizar as setas de direita e esquerda para mudar a direção e a barra de espaço para pular para a frente.

Obs.: tecnicamente você pode usar a seta para a frente para andar nesse sentido, mas ela anula o não-determinismo dessa ação.
-   ### Atalhos de teclado
    

-   1: aumenta a velocidade do Amongois (cuidado para não acelerar muito e exigir demais da sua máquina).
    
-   2: diminui a velocidade do Amongois.
    
-   3 a 7: tamanhos progressivamente menores de tela.
    

## Como é o formato das informações recebidas pelo jogo:

### Para o Estado:
Um estado é representado como um vetor binário que concatena a informação de que plataforma o personagem se encontra e para qual sentido ele está virado. Como são 24 plataformas possíveis, serão usados 5 dígitos em binário para essa representação. Para o sentido, por sua vez, serão usados dois dígitos, como segue:

> 00 = Norte
> 
> 01 = Leste
> 
> 10 = Sul
> 
> 11 = Oeste

Usando a função **get_state_reward()**, o servidor envia  o estado para o cliente. Abaixo, temos um exemplo de um estado enviado:

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXdxW_rsf_9jNcS_ziVscKOer1bv9HnyE_ZDbSmV1QnbtVR-zxGXxFsvtYsHrvD2b7ONEt92IYwwZluAOQHSIIoQ36MJ0uMeY3oPB5ZkUxCDjWNKZPNL4FZLfIWLfn0A92NC_QLgJvv9Lpe4WX0YUSVaNg_y0cC2-WtfKV8gLy-yhnagJPiK5Q?key=PZ_BjQO2n0pROWE1ICmcPA)

### Para a Recompensa:
A recompensa será um número inteiro negativo que irá variar de **-1** a **-14**, considerando o estado resultante do personagem, retornado pela ação ANTERIOR.

## Entrega do projeto:
Para a entrega do projeto, vocês devem enviar dois arquivos:
1.  O arquivo do cliente.py com o algoritmo de vocês.
2.  Um arquivo .txt que tenha a Q-table de vocês
    

### Observações:
Tentem deixar o arquivo do cliente.py de forma organizada e bem documentada. Quanto melhor documentado/organizado, mais fácil será para entender o que foi escrito e, com isso, melhor e mais rápida será a correção.

O arquivo com o **Q-table deve** *CONTER SOMENTE OS DADOS  ORDENADOS DE ACORDO COM O ESTADO CORRESPONDENTE, ou seja, NÃO É PARA CONTER O TÍTULO DAS COLUNAS E NEM O NÚMERO DAS LINHAS*.

A ordem das colunas na **Q-Table** deve ser [**Giro para Esquerda**, **Giro para Direita**, **Pulo para Frente**], respectivamente.

Por fim, a Q-table deve conter **TODOS OS POSSÍVEIS ESTADOS**. Como são **24** plataformas para **4 direções**, temos **96 estados** diferentes.

EXEMPLO: ver arquivo resultado.txt no repositório do github supracitado.
