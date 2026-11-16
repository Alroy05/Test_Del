/* @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&display=swap'); */
@import "tailwindcss";
@import '../node_modules/react-datepicker/dist/react-datepicker.css';
@import "@fontsource/inter/500.css";
@import "@fontsource/inter/600.css";
@import "@fontsource/inter/700.css";
@import "@fontsource/plus-jakarta-sans/600.css";
@import "@fontsource/plus-jakarta-sans/700.css";
@import "@fontsource/plus-jakarta-sans/800.css";
  
@custom-variant dark (&:where(.dark, .dark *));

body {
  font-family: "Inter", sans-serif;
 /* font-family: "Plus Jakarta Sans", sans-serif; */
  font-size: 14px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
@theme inline {
  --default-font-family: "Inter", sans-serif;
  --font-sans: "Inter", sans-serif;
  --font-arial: "Inter", sans-serif;
  --font-jakarta-sans: "Plus Jakarta Sans", sans-serif;
  /* --font-mono: "Roboto Mono", monospace; */
  --color-submit-btn: rgb(0, 51, 141);
  --color-highlight-blue: var(--color-blue-50);
  --color-dark-highlight-blue: var(--color-blue-700);
  --color-dot: rgb(0, 51, 141);

  --color-logo-blue: rgb(37, 83, 152);
  --color-kpmg-blue: rgb(0, 51, 141);
  --color-cobalt-blue: rgb(30, 73, 226);
  --color-dark-blue: rgb(12, 35, 60);
  --color-light-blue: rgb(172, 234, 255);
  --color-pacific-blue: rgb(0, 184, 245);
  --color-purple: rgb(114, 19, 234);
  --color-pink: rgb(253, 52, 156);

  --color-kpmg-default: rgb(0, 51, 141);
  --color-kpmg-light:  rgb(0, 94, 184);
  --color-kpmg-accent: rgb(71, 131, 224);
  --color-kpmg-deep: rgb(0, 52, 141);
  --color-kpmg-dark: rgb(15, 23, 42);

  --color-kpmg-header: rgb(11, 40, 110);

  --color-traffic-red: rgb(237, 33, 36);
  --color-traffic-yellow: rgb(241, 196, 77);
  --color-traffic-green: rgb(38, 153, 36);

  --color-blue: rgb(118, 210, 255);
  --color-dark-purple: rgb(81, 13, 188);
  --color-light-purple: rgb(180, 151, 255);
  --color-dark-pink: rgb(171, 13, 130);
  --color-light-pink: rgb(255, 163, 218);
  --color-dark-green: rgb(9, 142, 126);
  --color-green: rgb(0, 192, 174);
  --color-light-green: rgb(99, 235, 218);

  --color-grey1: rgb(51, 51, 51);
  --color-grey2: rgb(102, 102, 102);
  --color-grey3: rgb(152, 152, 152);
  --color-grey4: rgb(178, 178, 178);
  --color-grey5: rgb(229, 229, 229);
}

body {
  background: var(--background);
  color: var(--foreground);
}

@layer base {

  html {
    font-family: "Inter", sans-serif;
  }
  
  html:not(:has([data-layout="login"])) {
    font-size: 15px; 
  }

  /* Specifically for large laptop screens that aren't 4K */
  @media (max-width: 1600px) {
    html:not(:has([data-layout="login"])) {
      font-size: 14px;
    }
  }

  /* .table.table-bordered th {
    background-color: #096ed9;
    font-weight: 600;
    padding: 10px 12px; 
  }

  .text-primary {
    font-size: clamp(1.5rem, 2vw, 1.875rem); 
    color: #00338d;
  }
  
  .overall_residual_risk {
    font-size: 18px; 
    padding-top: 2px;
  } */

  .clip-cut {
    clip-path: polygon(0 0, 50% 0, 20% 100%, 0% 100%);
  }

  /* Hide scrollbar for Chrome, Safari and Opera */
  .no-scrollbar::-webkit-scrollbar {
    display: none;
  }

  /* Hide scrollbar for IE, Edge and Firefox */
  .no-scrollbar {
    -ms-overflow-style: none; /* IE and Edge */
    scrollbar-width: none; /* Firefox */
  }

input:-webkit-autofill,
textarea:-webkit-autofill,
select:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 1000px transparent inset !important;
  box-shadow: 0 0 0 1000px transparent inset !important;
  -webkit-text-fill-color: white !important;
  color: white !important;
  border-radius: inherit;
  background-clip: padding-box;
}
}

@keyframes slideInRight {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOutRight {
  0% {
    transform: translateX(0);
    opacity: 1;
  }
  100% {
    transform: translateX(100%);
    opacity: 0;
  }
}
