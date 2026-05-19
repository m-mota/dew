# Cosmic Heat Deluxe

Um jogo de nave futurista criado com **Pygame** e **Pygbag**, rodando diretamente no navegador!

## Jogar Agora

Abra o arquivo `index.html` no seu navegador para jogar! Ou acesse via GitHub Pages.

## Requisitos do Sistema

- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Sem instalacao necessaria!
- Funciona em desktop e tablets

## Controles

| Acao | Tecla |
|------|-------|
| **Mover Nave** | Setas ou WASD |
| **Atirar** | ESPACO |
| **Pausar** | P |
| **Reiniciar** | R (pos game over) |
| **Comecar** | ENTER (menu) |
| **Sair** | ESC |

## Objetivos do Jogo

- **Derrote inimigos** para ganhar pontos
- **Evite meteoros** e tiros inimigos
- **Colete power-ups** para melhorias (vida, ammo, triplo tiro, escudo)
- **Enfrente o Boss** final para vencer!
- **Suba de nivel** a medida que aumenta sua pontuacao

##   Sistema de Jogo

### Entidades
- **Nave (Jogador)**: 100 HP, velocidade 7
- **Inimigos**: Dificuldade aumenta por n vel
- **Meteoros**: Objetos destrutivos
- **Boss**: Boss final com 2 fases (normal e raiva)
- **Power-ups**: Vida, Ammo, Triplo Tiro, Escudo, Pontos

### Pontua  o
- Inimigo: 30 + (n vel   5) pontos
- Meteoro: 15 pontos
- Tiro Boss: 10 pontos
- Boss derrotado: 1000 pontos
- Combo: B nus adicional

##   Como Hospedar no GitHub Pages

1. **Fa a upload do reposit rio para GitHub**:
   ```bash
   git add .
   git commit -m "Jogo Cosmic Heat Deluxe"
   git push origin main
   ```

2. **Ative GitHub Pages**:
   - V  para Settings   Pages
   - Selecione `main` branch
   - Aguarde o deploy

3. **Acesse seu jogo**:
   - `https://seu-usuario.github.io/dew/`

##   Estrutura do Projeto

```
dew/
    index.html      # Arquivo principal (jogo rodan no navegador)
    main.py         # C digo Python original (Pygame)
    README.md       # Este arquivo
    .gitignore      # Arquivos ignorados pelo Git
```

##    Tecnologias

- **Pygame**: Engine do jogo
- **PyScript**: Executa Python no navegador
- **HTML5/CSS3**: Interface
- **Canvas**: Renderiza  o gr fica

##   Limita  es Conhecidas

- Performance pode variar em navegadores mais antigos
- Pygame tem suporte limitado no navegador via Pyodide
- Alguns features avan ados podem n o funcionar 100%

##   Licen a

Livre para usar e modificar!

##     Desenvolvimento

Criado com    em Python

---

**Divirta-se jogando!**   
