# 🚀 Cosmic Heat Deluxe ✨

Um jogo de nave futurista criado com **Pygame** e **PyScript**, rodando diretamente no navegador!

## 🎮 Jogar Agora

Abra o arquivo `index.html` no seu navegador para jogar! Ou acesse via GitHub Pages (após fazer push).

## 📋 Requisitos do Sistema

- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Sem instalação necessária!
- Funciona em desktop e tablets

## ⌨️ Controles

| Ação | Tecla |
|------|-------|
| **Mover Nave** | Setas ou WASD |
| **Atirar** | ESPAÇO |
| **Pausar** | P |
| **Reiniciar** | R (após game over) |
| **Começar** | ENTER (menu) |
| **Sair** | ESC |

## 🎯 Objetivos do Jogo

- **Derrote inimigos** para ganhar pontos
- **Evite meteoros** e tiros inimigos
- **Colete power-ups** para melhorias (vida, ammo, triplo tiro, escudo)
- **Enfrente o Boss** final para vencer!
- **Suba de nível** à medida que aumenta sua pontuação

## 📊 Sistema de Jogo

### Entidades
- **Nave (Jogador)**: 100 HP, velocidade 7
- **Inimigos**: Dificuldade aumenta por nível
- **Meteoros**: Objetos destrutivos
- **Boss**: Boss final com 2 fases (normal e raiva)
- **Power-ups**: Vida, Ammo, Triplo Tiro, Escudo, Pontos

### Pontuação
- Inimigo: 30 + (nível × 5) pontos
- Meteoro: 15 pontos
- Tiro Boss: 10 pontos
- Boss derrotado: 1000 pontos
- Combo: Bônus adicional

## 🔧 Como Hospedar no GitHub Pages

1. **Faça upload do repositório para GitHub**:
   ```bash
   git add .
   git commit -m "Jogo Cosmic Heat Deluxe"
   git push origin main
   ```

2. **Ative GitHub Pages**:
   - Vá para Settings → Pages
   - Selecione `main` branch
   - Aguarde o deploy

3. **Acesse seu jogo**:
   - `https://seu-usuario.github.io/dew/`

## 📁 Estrutura do Projeto

```
dew/
├── index.html      # Arquivo principal (jogo rodan no navegador)
├── main.py         # Código Python original (Pygame)
├── README.md       # Este arquivo
└── .gitignore      # Arquivos ignorados pelo Git
```

## 🛠️ Tecnologias

- **Pygame**: Engine do jogo
- **PyScript**: Executa Python no navegador
- **HTML5/CSS3**: Interface
- **Canvas**: Renderização gráfica

## 🐛 Limitações Conhecidas

- Performance pode variar em navegadores mais antigos
- Pygame tem suporte limitado no navegador via Pyodide
- Alguns features avançados podem não funcionar 100%

## 📝 Licença

Livre para usar e modificar!

## 👨‍💻 Desenvolvimento

Criado com ❤️ em Python

---

**Divirta-se jogando!** 🎮✨
