/* Tema central do site — carregado por todas as paginas (PT e EN).
 *
 * Em vez de trocar classe por classe nos 12 arquivos HTML, remapeamos as
 * escalas de cor do Tailwind. Assim `text-teal-500` continua no markup, mas
 * passa a render izar a cor da marca. Trocar a identidade do site vira editar
 * este arquivo, e nada mais.
 *
 * `teal`  -> azul-periwinkle da marca (alinhado ao perfil do GitHub)
 * `zinc`  -> neutro levemente azulado, que combina com o accent
 *
 * Contraste conferido: accent 600 em branco = 6,19:1 e accent 400 no fundo
 * escuro = 7,87:1, ambos acima do minimo AA (4,5:1).
 */
(function () {
  var brand = {
    50:  '#eef1fe',
    100: '#e0e6fd',
    200: '#c6d0fc',
    300: '#a9b6fd',
    400: '#8da2fb',  // texto de destaque no modo escuro
    500: '#6475ee',
    600: '#4451d6',  // texto de destaque no modo claro
    700: '#3a45b8',
    800: '#303a93',
    900: '#2b3375',
  };

  var neutral = {
    50:  '#f8f9fb',
    100: '#f1f2f6',
    200: '#e5e7ee',
    300: '#cbcfdb',
    400: '#9ba1b4',
    500: '#767c8f',
    600: '#565c6e',
    700: '#3f4452',
    800: '#262a35',
    900: '#161922',
    950: '#0e1016',
  };

  window.tailwind = window.tailwind || {};
  window.tailwind.config = {
    darkMode: 'class',
    theme: {
      extend: {
        colors: {
          teal: brand,   // apelido: mantem o markup existente funcionando
          brand: brand,
          zinc: neutral,
        },
        fontFamily: {
          sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
          mono: ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
        },
      },
    },
  };
})();
