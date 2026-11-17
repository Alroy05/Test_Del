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

.animate-slide-in-right {
  animation: slideInRight 2s ease forwards;
}

.animate-slide-out-right {
  animation: slideOutRight 2s ease forwards;
}

@keyframes slideDown {
  0% {
    transform: translateY(-100px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideUp {
  0% {
    transform: translateY(0);
    opacity: 1;
  }
  100% {
    transform: translateY(-100px);
    opacity: 0;
  }
}

.animate-slide-down {
  animation: slideDown 0.4s ease-out forwards;
}

.animate-slide-up {
  animation: slideUp 0.4s ease-in forwards;
}

@keyframes zoomIn {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes zoomOut {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(0.7);
  }
}

.modal-zoom-in {
  animation: zoomIn 0.2s ease-out forwards;
}

.modal-zoom-out {
  animation: zoomOut 1s ease-in forwards;
}

/* Collapsible animation classes */
.collapsible {
  overflow: hidden;
  transition: max-height 0.4s ease, opacity 0.4s ease, transform 0.4s ease;
}

.collapsible-enter {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.collapsible-enter-active {
  max-height: 1000px;
  opacity: 1;
  transform: translateY(0);
}

.collapsible-exit {
  max-height: 1000px;
  opacity: 1;
  transform: translateY(0);
}

.collapsible-exit-active {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.badge {
    border-radius: 30px !important;
    box-shadow: 0 4px 6px rgba(50, 50, 93, .11), 0 1px 3px rgb(0 0 0 / 8%) !important;
    font-weight: 500 !important;
    letter-spacing: .5px !important;
    padding: 7px 9px !important;
    color: rgb(255, 255, 255);
    background-color: rgb(30, 73, 226);
    font-size: 12px;
}

.parent-bg{
    background-color: #bcd8f1
}

.view-bg{
    background-color: #d5e4f1
}

.hide22{
    display: none;
}

.show22{
    display: block;
}

/* .table > thead > tr > td{
    background-color : #1E49E2;
} */

.badge-edit{
    line-height: 15px !important;
    margin-left: 5px !important;
    padding: 3px!important;
    cursor: pointer!important;
    color: white !important;
    background-color: #6D2077!important;
    border-color: #6D2077!important;
    text-align: center!important;
    font-size: 14px!important;
    letter-spacing: .4px!important;
    box-shadow: 0 4px 6px rgba(50, 50, 93, .11), 0 1px 3px rgba(0, 0, 0, .08)!important;
}

.view-edit-icon{
    color: white !important;
    background-color: #00338D;
    padding-left: .5rem;
    padding-right: .5rem;
    text-align: center;
    font-size: 14px;
    line-height: 26px;
    padding: 5px 23px;
    letter-spacing: .4px;
    box-shadow: 0 4px 6px rgba(50, 50, 93, .11), 0 1px 3px rgba(0, 0, 0, .08);
}

.update-edit-button{
    color: white !important;
    background-color: #6D2077;
    border-color: #6D2077;
    padding-left: .5rem;
    padding-right: .5rem;
    text-align: center;
    font-size: 14px;
    line-height: 26px;
    padding: 5px 23px;
    letter-spacing: .4px;
    box-shadow: 0 4px 6px rgba(50, 50, 93, .11), 0 1px 3px rgba(0, 0, 0, .08);
}

.update-edit-button:hover{
    color: white !important;
    background-color: #6D2077;
    border-color: #6D2077;
    padding-left: .5rem;
    padding-right: .5rem;
    text-align: center;
    font-size: 14px;
    line-height: 26px;
    padding: 5px 23px;
    letter-spacing: .4px;
    box-shadow: 0 4px 6px rgba(50, 50, 93, .11), 0 1px 3px rgba(0, 0, 0, .08);
}

.top-bg{
    background-color: #526069 !important;
}

.top-color{
    color: #fff!important;
}

.bg-light, .btn-light {
    background-color: #E5E5E5 !important;
    /* color: white; */
}

.recharts-wrapper svg:focus {
  outline: none;
}

.text-danger{
  color: #dc2626; /* Tailwind's red-600 */
  font-size: 12px;
}

.table.table-bordered {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ccc;
  font-size: 15px;
}

.table.table-bordered th,
.table.table-bordered td {
  border: 1px solid #ccc;
  padding: 10px 14px;
  text-align: left;
  vertical-align: top;
}

.table.table-bordered th {
  background-color: #096ed9;
  font-weight: 600;
  padding: 15px 12px
}

/* .table th {
  background-color: #096ed9;
  padding: 8px 10px;
  width: 100%;
  margin-top: 2px;
} */

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  background-color: #096ed9;
  padding: 12px 10px;
  color: white;
  text-align: left;
  margin-bottom: 2px;
}

.dark .table.table-bordered th {
  background-color: #00338D; /* Tailwind's neutral-800 */
  color: #f3f4f6; /* Tailwind's gray-100 */
}

.dark .table.table-bordered td {
  border-color: #4b5563; /* Tailwind's gray-600 */
  color: #e5e7eb; /* Tailwind's gray-200 */
}

.table.table-bordered th.bg-info {
  background-color: #3498db;
  color: #ffffff;
}

.dark .table.table-bordered th.bg-info {
  background-color: #3498db;
  color: #ffffff;
}

.font-weight-bold {
  font-weight: bold;
  padding-top: 2px;
  padding-bottom: 2px;
}


label {
    font-weight: 500;
    margin-bottom: .5rem;
    display: inline-block;
}

/* Dropdown */
.custom-dropdown {
  width: 100%;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
  background-color: #f9f9f9;

  /* Remove all arrows */
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;

  /* Remove custom arrow image */
  background-image: none;
  background-repeat: none;
  background-position: unset;
  background-size: unset;
}

.custom-dropdown:hover {
  border-color: #888;
}

.custom-dropdown:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* Optional: color-coded options */
.status-implemented { background-color: #A8D08D; }
.status-partial { background-color: #FFE599; }
.status-gap { background-color: #F4B083; }
.status-not-assessed { background-color: #D0CECE; }

/* Wrapper */
.dropdown-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
}

/* Remove custom arrow from wrapper */
.dropdown-wrapper::after {
  content: none;
}

.comment-section {
  width: 75%;
  padding: 4px;
  border: 1px solid #ccc;
}

.overall_residual_risk {
  font-size: 21px;
  padding-top: 2px;
}

.table-top-th{
  padding-left: 0.375rem;   /* px-1.5 */
  padding-right: 0.375rem;  /* px-1.5 */
  padding-top: 1rem;        /* py-4 */
  padding-bottom: 1rem;     /* py-4 */
  text-align: left;         /* text-left */
  font-size: 12px;          /* text-[12px] */
  font-weight: 500;         /* font-medium */
  color: #ffffff;           /* text-white */
  border-collapse: collapse;/* border-collapse */
  border: 1px solid #d1d5db;/* border border-gray-300 */
  letter-spacing: 0.05em;   /* tracking-wider */
}

/* Dark mode border */
@media (prefers-color-scheme: dark) {
  .table-top-th {
    border-color: #404040; /* dark:border-neutral-700 */
  }
}

.pen-test-th{
    text-align: left;            /* text-left */
    font-weight: 600;            /* font-semibold */
    color: #374151;              /* text-gray-700 */
    padding-left: 1rem;          /* px-4 */
    padding-right: 1rem;
    padding-top: 0.75rem;        /* py-3 */
    padding-bottom: 0.75rem;
    width: 50%;                  /* w-1/2 */
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
    .pen-test {
        color: #ffffff;          /* dark:text-white */
    }
}

.pen-test-tr{
    border-bottom: 1px solid #e5e7eb; /* border-b + border-gray-200 */
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
    .pen-test-tr{
        border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* dark:border-white/10 */
    }
}

.pen-test-table {
    width: 100%;                  /* table */
    border-collapse: collapse;    /* table */
    border: 1px solid #dee2e6;    /* table-bordered */
    font-size: 13px;           /* table-lg (approx large size) */
}

.pen-test-table th,
.pen-test-table td {
    border: 1px solid #dee2e6;    /* table-bordered */
    padding: 0.75rem;             /* typical Bootstrap padding */
}

/* table-striped */
.pen-test-table tbody tr:nth-child(odd) {
    background-color: #f8f9fa;
}

.common-th{
  padding-left: 1.5rem;   /* px-6 */
  padding-right: 1.5rem;  /* px-6 */
  padding-top: 1rem;      /* py-4 */
  padding-bottom: 1rem;   /* py-4 */
  text-align: left;       /* text-left */
  font-size: 13px;        /* text-[13px] */
  font-weight: bold;      /* font-bold */
  color: #ffffff;         /* text-white */
  letter-spacing: 0.05em; /* tracking-wider */
}

.common-tbody{
  border-top-width: 1px; /* divide-y */
  border-color: rgba(212, 212, 212, 0.8); /* divide-neutral-300/80 */
}

.dark .common-tbody{
  border-color: #262626; /* dark:divide-neutral-800 */
}


.common-tbody-tr {
  background-color: rgba(219, 234, 254, 0.5); /* bg-blue-100/50 */
  transition-property: background-color;      /* transition-colors */
  transition-duration: 150ms;                 /* default Tailwind duration */
}

.dark .common-tbody-tr {
  background-color: #171717; /* dark:bg-neutral-900 */
}

.common-tbody-tr:hover {
  background-color: #dbeafe; /* hover:bg-blue-100 */
}

.dark .common-tbody-tr:hover {
  background-color: rgba(64, 64, 64, 0.5); /* dark:hover:bg-neutral-700/50 */
}


.common-tbody-td {
  padding-left: 1.5rem;   /* px-6 */
  padding-right: 1.5rem;  /* px-6 */
  padding-top: 0.75rem;   /* py-3 */
  padding-bottom: 0.75rem;/* py-3 */
  white-space: nowrap;    /* whitespace-nowrap */
  font-size: 13px;        /* text-[13px] */
  color: #171717;         /* text-neutral-900 */
}

.dark .common-tbody-td {
  color: #f5f5f5; /* dark:text-neutral-100 */
}

.table > thead > tr > th{
    background-color : #1E49E2
}

.link{
  color:#00338d
}

.subtable-testingo {
  /* px-2: padding-left and padding-right = 0.5rem (8px) */
  padding-left: 0.5rem;
  padding-right: 0.5rem;

  /* py-3: padding-top and padding-bottom = 0.75rem (12px) */
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;

  /* text-gray-800: text color */
  color: #1f2937; /* Gray 800 */

  /* border: 1px solid */
  border-width: 1px;
  border-style: solid;

  /* border-gray-300: border color */
  border-color: #d1d5db; /* Gray 300 */
}

.text-primary{
  font-size: 2.143rem;
  color: #00338d;
}

.text-primary-sub{
  font-size: 1.6rem;
  color: #00338d;
}

.label-custom{
  font-weight: 500;
  margin-bottom: .5rem;
  font-size: 13px;
}

.btn-info-custom{
  background-color: var(--color-submit-btn) !important;
  border-color: var(--color-submit-btn);
}

.btn-primary-custom{
  background-color: #00338d;
  color: white;
}

.btn-danger-custom {
    background-color: #ED2124;
    border-color: #ED2124;
}

/* Custom DatePicker Wrapper Styles */
.custom-datepicker-wrapper {
  width: 100%;
}

/* Custom DatePicker Input Styles */
.custom-datepicker {
  width: 100%;
  font-size: 0.875rem;
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid;
  transition: all 0.15s ease;
}

.custom-datepicker:focus {
  outline: none;
  border-color: #3b82f6;
}

/* Light mode styles */
.custom-datepicker {
  background-color: white;
  color: black;
  border-color: #d1d5db;
}


/* Error state */
.custom-datepicker.error {
  border-color: #ef4444;
}

/* React DatePicker Calendar Styling */
.react-datepicker-wrapper {
  width: 100%;
}

.react-datepicker {
  font-family: inherit;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  overflow: hidden;
}

.react-datepicker__header {
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}

.react-datepicker__current-month,
.react-datepicker__day-name {
  color: #111827;
}


.react-datepicker__day {
  color: #374151;
}


.react-datepicker__day:hover {
  background-color: #e5e7eb;
}

.react-datepicker__day--selected,
.react-datepicker__day--keyboard-selected {
  background-color: #3b82f6;
  color: white;
}

.react-datepicker__day--disabled {
  color: #9ca3af;
}

.react-datepicker__navigation-icon::before {
  border-color: #6b7280;
}

.react-datepicker__triangle {
  display: none;
}

.first-div-color{
  color:#00338d;
}

/* Milestone/Timeline Styles */

/* Form elements */
.form-label {
  font-size: 11px;
  font-weight: 700;
  color: #475569;
  letter-spacing: 0.03em;
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dark .form-label {
  color: #cbd5e1;
}

.form-input {
  width: 100%;
  height: 36px;
  padding: 0 1rem;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
  background-color: #fff;
  font-size: 13px;
  transition: all 0.2s ease;
  color: #1e293b;
}

.dark .form-input {
  border-color: #334155;
  background-color: #1e293b;
  color: #f1f5f9;
}

.form-input:focus {
  outline: none;
  border-color: #00338D;
  box-shadow: 0 0 0 4px rgba(0, 51, 141, 0.1);
}

.form-input.error {
  border-color: #ef4444;
}

.form-input-default {
  width: 100%;
  height: 36px;
  padding: 0 1rem;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
  background-color: #fff;
  font-size: 13px;
  transition: all 0.2s ease;
  color: #1e293b;
}

.dark .form-input-default {
  border-color: #334155;
  background-color: #1e293b;
  color: #f1f5f9;
}

.form-input-default:focus {
  outline: none;
  border-color: #00338D;
  box-shadow: 0 0 0 4px rgba(0, 51, 141, 0.1);
}

.form-input-default.error {
  border-color: #ef4444;
}

/* Milestone container */
.milestone-section .milestone-container {
  display: flex;
  gap: 1.5rem;
  position: relative;
  width: 100%;
}

.milestone-section .milestone-track {
  width: 24px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  padding-top: 14px;
}

.milestone-section .milestone-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e2e8f0;
  z-index: 10;
  left: 50%;
  transform: translateX(-50%);
}

.dark .milestone-section .milestone-line {
  background: #334155;
}

/* Milestone dot states */
.milestone-section .milestone-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #cbd5e1;
  border: 2px solid #fff;
  z-index: 20;
  position: relative;
  transition: all 0.4s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dark .milestone-section .milestone-dot {
  background: #334155;
  border-color: #020617;
}

.milestone-section .milestone-dot svg {
  display: none;
  width: 8px;
  height: 8px;
}

/* Open state */
.milestone-section .milestone-step.is-open .milestone-dot {
  background: #00338D;
  transform: scale(1.4);
  border-color: #fff;
  box-shadow: 0 0 12px rgba(0, 51, 141, 0.4);
}

.dark .milestone-section .milestone-step.is-open .milestone-dot {
  background: #ADCBFB;
  border-color: #020617;
  box-shadow: 0 0 12px rgba(173, 203, 251, 0.4);
}

/* Completed state */
.milestone-section .milestone-step.is-completed .milestone-dot {
  background-color: #E5F5E0 !important;
  border: 1.5px solid #059669 !important;
  width: 18px;
  height: 18px;
  transform: scale(1);
}

.dark .milestone-section .milestone-step.is-completed .milestone-dot {
  background-color: #F0FDF4 !important;
}

.milestone-section .milestone-step.is-completed .milestone-dot svg {
  display: block !important;
  color: #059669 !important;
}

/* Content area */
.milestone-section .milestone-content-area {
  flex: 1;
  padding-bottom: 1.5rem;
  width: 100%;
}

.milestone-section .milestone-card {
  border: 1px solid #e2e8f0;
  background: #fff;
  border-radius: 8px;
  overflow: visible;
  width: 100%;
}

.dark .milestone-section .milestone-card {
  border-color: #334155;
  background: #0f172a;
}

/* Header */
.milestone-section .milestone-header {
  padding: 0.85rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  background: #fff;
  color: #475569;
  transition: all 0.3s ease;
  border-radius: 8px;
  min-height: 48px;
  width: 100%;
}

.dark .milestone-section .milestone-header {
  background: #1e293b !important;
  color: #f1f5f9 !important;
  border: 1px solid #334155;
}

.milestone-section .milestone-header.active {
  background: #f0f4f9 !important;
  color: #00338D !important;
  border-radius: 8px 8px 0 0;
}

.dark .milestone-section .milestone-header.active {
  background: #334155 !important;
  color: #ADCBFB !important;
  border-color: #64748b;
  border-bottom: none;
}

.milestone-section .milestone-title {
  font-weight: 700;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

/* Body */
.milestone-section .milestone-body {
  padding: 0 1.5rem;
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-top: 1px solid transparent;
  width: 100%;
}

.milestone-section .milestone-body.open {
  padding: 1.5rem;
  max-height: 2500px;
  opacity: 1;
  border-top-color: #f1f5f9;
  overflow: visible;
}

.dark .milestone-section .milestone-body.open {
  border-top-color: #334155;
  background: #0f172a;
}

/* Step icon */
.milestone-section .step-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.dark .milestone-section .step-icon {
  background: #0f172a;
  color: #cbd5e1;
}

.milestone-section .active .step-icon {
  background: rgba(0, 51, 141, 0.1);
  color: #00338D;
  transform: scale(1.1);
}

.dark .milestone-section .active .step-icon {
  background: rgba(173, 203, 251, 0.2);
  color: #ADCBFB;
}


/* Continue button */
.btn-continue {
  background-color: transparent;
  color: #00338D;
  border: 1.2px solid #00338D;
  background-color: var(--color-submit-btn);
  color: white;
  border: var(--color-submit-btn);;
  padding: 0.35rem 1.25rem;
  font-weight: 700;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-radius: 9999px;
  border-radius: 5px;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  gap: 3px;
}

.btn-continue:hover {
  background-color: #00338D;
  background-color: var(--color-submit-btn);
  color: white;
  transform: translateY(-1px);
}

.dark .btn-continue {
  color: #ADCBFB;
  border-color: #ADCBFB;
  color: white;
  border-color: white;
}

.dark .btn-continue:hover {
  background-color: #ADCBFB;
  color: #00338D;
  background-color: var(--color-submit-btn);
  color: white;
}

/* Warning note */
.warning-note {
  font-size: 11px;
  font-weight: 600;
  color: #b91c1c;
  padding: 12px;
  background: #fef2f2;
  border-radius: 6px;
  margin-top: 8px;
  border: 1px solid #fee2e2;
}

.dark .warning-note {
  background: #450a0a;
  color: #fecaca;
  border-color: #7f1d1d;
}

/* Alias badge */
.alias-badge {
  background-color: #e0f2fe;
  color: #00338D;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid #bae6fd;
  text-transform: lowercase;
}

.dark .alias-badge {
  background-color: #0c4a6e;
  color: #7dd3fc;
  border-color: #075985;
}

/* Helper text */
.helper-text {
  font-size: 12px;
  color: rgb(0, 51, 141);
  margin-top: 2px;
  /* font-style: italic; */
  font-weight: bold;
  display: block;
  white-space: pre-line;
}

.dark .helper-text {
  color: #94a3b8;
}

/* Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-in;
}

/* Additional styles for Request Edit page */
.form-label {
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  /* letter-spacing: 0.03em; */
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dark .form-label {
  color: #cbd5e1;
}

.form-input {
  width: 100%;
  height: 36px;
  padding: 0 1rem;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
  background-color: #fff;
  font-size: 13px;
  transition: all 0.2s ease;
  color: #1e293b;
}

.dark .form-input {
  border-color: #334155;
  background-color: #1e293b;
  color: #f1f5f9;
}

.form-input:focus {
  outline: none;
  border-color: #00338D;
  box-shadow: 0 0 0 4px rgba(0, 51, 141, 0.1);
}

.form-input.error {
  border-color: #ef4444;
}

.warning-note {
  font-size: 11px;
  font-weight: 600;
  color: #00338D;
  padding: 5px;
  background: #f4f7fc;
  border-radius: 6px;
  margin-top: 8px;
  border: 1px solid #87b3ff;
}

.dark .warning-note {
  background: #0b2450;
  color: #f4f7fc;
  border-color: #00338D;
}

.alias-badge {
  background-color: #e0f2fe;
  color: #00338D;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid #bae6fd;
  text-transform: lowercase;
}

.dark .alias-badge {
  background-color: #0c4a6e;
  color: #7dd3fc;
  border-color: #075985;
}

/* datepicker ui */
.react-datepicker {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1) !important;
    background-color: white !important;
  }
  .dark .react-datepicker {
    background-color: #1E293B !important;
    border-color: #334155 !important;
    color: #F1F5F9 !important;
  }
  .react-datepicker__header {
    background-color: #F8FAFC !important;
    border-bottom: 1px solid #E2E8F0 !important;
    border-top-left-radius: 12px !important;
    border-top-right-radius: 12px !important;
    padding-top: 12px !important;
  }
  .dark .react-datepicker__header {
    background-color: #0F172A !important;
    border-color: #334155 !important;
  }
  .react-datepicker__current-month, .react-datepicker__day-name {
    color: #1E293B !important;
    font-weight: 700 !important;
  }
  .dark .react-datepicker__current-month, .dark .react-datepicker__day-name {
    color: #F1F5F9 !important;
  }
  .react-datepicker__day {
    color: #475569 !important;
    border-radius: 8px !important;
  }
  .dark .react-datepicker__day {
    color: #94A3B8 !important;
  }
  .react-datepicker__day:hover {
    background-color: #EFF6FF !important;
    color: #00338D !important;
  }
  .dark .react-datepicker__day:hover {
    background-color: #334155 !important;
    color: white !important;
  }
  .react-datepicker__day--selected {
    background-color: #00338D !important;
    color: white !important;
    font-weight: 700 !important;
  }
  .dark .react-datepicker__day--selected {
    background-color: #4783E0 !important;
  }
  .react-datepicker__navigation-icon::before {
    border-color: #94A3B8 !important;
  }

  .chart-margin{
    margin-top: -50px;
  }

  .glass-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  }

  .glass-card-view {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  }

  .dark .glass-card-view { background: #0F172A;}

  .dark .glass-card { background: #0F172A; border-color: #1E293B; }

  .inline-comment {
      font-size: 13px; color: #64748b; line-height: 1.4; padding: 8px 12px; background: #F1F5F9; border-left: 4px solid #CBD5E1; border-radius: 4px 10px 10px 4px; margin-top: 6px; max-width: 95%;
  }
  .dark .inline-comment { background: #0f172a; border-left-color: #334155; color: #94a3b8; }

  .comment-title { 
      display: block; font-size: 13px; letter-spacing: 0.05em; color: #94a3b8; margin-bottom: 2px; text-transform: capitalize;
  }
  .dark .comment-title { color: #64748b; }

  .tab-btn {
      padding: 10px 16px; font-size: 13px; font-weight: 700; border-bottom: 2px solid transparent; transition: all 0.2s; cursor: pointer; white-space: nowrap;
  }
  .tab-btn:hover { color: #00338D; }
  .tab-btn.active { color: #00338D; border-bottom-color: #00338D; background: rgba(0, 51, 141, 0.03); }
  .dark .tab-btn.active { color: #4783E0; border-bottom-color: #4783E0; background: rgba(255, 255, 255, 0.03); }

   .tab-btn-env {
      padding: 10px 16px; font-size: 13px; font-weight: 700; border-bottom: 2px solid transparent; transition: all 0.2s; cursor: pointer; white-space: nowrap;
  }
  .tab-btn-env.active { color: #00338D; border-bottom-color: #00338D; background: rgba(0, 51, 141, 0.03); }
  .dark .tab-btn-env.active { color: #4783E0; border-bottom-color: #4783E0; background: rgba(255, 255, 255, 0.03); }

  .section-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #f1f5f9;
  }
  .dark .section-header { border-bottom-color: #1e293b; }

.risk-high, .th-high, .High { color: #ef4444 !important; font-weight: 700; }
.risk-medium, .th-medium, .Medium { color: #f59e0b !important; font-weight: 700; }
.risk-low, .th-low, .Low { color: #10b981 !important; font-weight: 700; }
.risk-info, .th-info, .Informational { color: #3b82f6 !important; font-weight: 700; }

.timeline-container {
    border-left: 2px solid #E2E8F0;
    margin-left: 8px;
    padding-left: 24px;
    position: relative;
}
.dark .timeline-container { border-left-color: #334155; }

.history-collapsible { max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }
.history-collapsible.show { max-height: 2000px; margin-top: 1.5rem; }

.comment-entry { position: relative; margin-bottom: 28px; }
.comment-entry::before {
  content: ''; position: absolute; left: -30px; top: 6px;
  width: 10px; height: 10px; background: white;
  border: 2px solid #00338D; border-radius: 50%; z-index: 10;
}
.dark .comment-entry::before { background: #0F172A; border-color: #93C5FD; }

.progress-container {
    width: 100%;
    height: 8px;
    background-color: #F1F5F9;
    border-radius: 99px;
    overflow: hidden;
    margin: 20px 0;
    position: relative;
}
.dark .progress-container { background-color: #1E293B; }

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #00338D, #00B8F5);
    width: 0%;
    border-radius: 99px;
    transition: width 3s ease-in-out;
}

.success-tick {
    display: none;
    color: #10b981;
    font-size: 2.5rem;
    animation: scaleIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

@keyframes scaleIn {
    from { transform: scale(0); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.btn-download {
    background-color: rgb(0, 52, 141);
    color: white;
    padding: 8px 8px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 13px;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    border: none;
}
.btn-download:hover { opacity: 0.9; transform: translateY(-1px); }

.btn-close {
    background-color: #F1F5F9;
    color: #475569;
    padding: 8px 8px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 13px;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    border: 1px solid #E2E8F0;
}
.dark .btn-close { background-color: #1E293B; color: #94A3B8; border-color: #334155; }
.btn-close:hover { background-color: #E2E8F0; }
.dark .btn-close:hover { background-color: #334155; }

.wrap{
  overflow-wrap: break-word;
}

@keyframes wave {
    0%, 100% { 
        transform: scaleY(0.3); 
        opacity: 0.5; 
    }
    50% { 
        transform: scaleY(1); 
        opacity: 1; 
    }
}

.integrity-trace {
    width: 80px;
    height: 35px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.integrity-trace div {
    flex: 1;
    height: 100%;
    animation: wave 1.2s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
    animation-fill-mode: backwards;
    transform: scaleY(0.3);
    opacity: 0.5;
}

.gisg-layout {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: rgb(12, 35, 60);
  color: white;
}

.focal-glow {
  position: absolute;
  filter: blur(120px);
  pointer-events: none;
  border-radius: 9999px;
}

@keyframes move-glow {
  from {
    transform: translate(0, 0) scale(1);
  }

  to {
    transform: translate(80px, 60px) scale(1.1);
  }
}

.datepicker-popper {
  z-index: 9999 !important;
}

.gisg-input {
  background: rgba(255, 255, 255, 0.03);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  color: white;
  transition: all 0.3s ease;
  height: 42px;
}

.gisg-input:focus {
  border-color: rgb(162, 234, 255);
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 3px rgba(162, 234, 255, 0.06);
  outline: none;
}

.gisg-input::placeholder {
  color: rgba(255, 255, 255, 0.15);
}

.gisg-btn-primary {
  background: linear-gradient(135deg, rgb(30, 73, 226) 0%, rgb(0, 51, 141) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  color: white;
  font-weight: 700;
}

.gisg-btn-primary:hover {
  filter: brightness(1.2);
  box-shadow: 0 10px 30px rgba(30, 73, 226, 0.3);
}

.gisg-btn-ghost {
  background: rgba(255, 255, 255, 0.03);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.85);
  font-weight: 600;
}

.gisg-btn-ghost:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgb(162, 234, 255);
}

.gisg-or-line {
  height: 1px;
  background: linear-gradient(to right, transparent, rgb(162, 234, 255), transparent);
  opacity: 0.2;
}

.gisg-label {
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: rgb(162, 234, 255);
}

.gisg-section-title {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: rgba(255, 255, 255, 0.3);
}

.grain-overlay {
  position: fixed;
  inset: 0;
  z-index: 5;
  opacity: 0.055;
  pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}
.otp-cell {
    background: rgba(255, 255, 255, 0.03);
    border: 0.5px solid rgba(255, 255, 255, 0.12);
    color: white;
    transition: all 0.3s ease;
    height: 56px;
    width: 100%;
    aspect-ratio: 1;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    border-radius: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.otp-cell:focus {
    border-color: rgb(162, 234, 255);
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 0 3px rgba(162, 234, 255, 0.06);
    outline: none;
}
.otp-cell.filled {
    border-color: rgba(162, 234, 255, 0.4);
}

.main-card {
  background: linear-gradient(145deg, rgba(9, 22, 37, 0.98) 0%, rgba(12, 35, 60, 0.88) 100%);
  backdrop-filter: blur(60px) saturate(180%);
  -webkit-backdrop-filter: blur(60px) saturate(180%);
  border: 1px solid rgba(162, 234, 255, 0.1);
  box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.7), inset 0 1px 1px rgba(255, 255, 255, 0.04);
  border-radius: 32px;
}

.landing-card {
  background: white;
  border: 1px solid rgba(162, 234, 255, 0.1);
  border-radius: 32px;
}

.dark .landing-card {
  background: linear-gradient(145deg, rgba(9, 22, 37, 0.98) 0%, rgba(12, 35, 60, 0.88) 100%);
  backdrop-filter: blur(60px) saturate(180%);
  -webkit-backdrop-filter: blur(60px) saturate(180%);
  border: 1px solid rgba(162, 234, 255, 0.1);
  box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.7), inset 0 1px 1px rgba(255, 255, 255, 0.04);
  border-radius: 32px;
}

.spectrum-text {
  background: linear-gradient(to right,
      rgb(162, 234, 255), rgb(0, 184, 245), rgb(118, 210, 255),
      #FFFFFF, rgb(180, 151, 255), rgb(255, 163, 218),
      rgb(162, 234, 255));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes pulse-pink {

  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }

  50% {
    transform: scale(1.15);
    opacity: 0.7;
  }
}

.pink-pulse {
  animation: pulse-pink 3s ease-in-out infinite;
}

input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
  display: none;
}

input[type="password"]::-webkit-textfield-decoration-container {
  display: none;
}


input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0px 1000px transparent inset !important;
  box-shadow: 0 0 0px 1000px transparent inset !important;
  -webkit-text-fill-color: white !important; 
  transition: background-color 9999s ease-in-out 0s;
}

.display-none{
  display: none;
}

.status-tag {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: bold;
  text-transform: uppercase;
}

.upload-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    border: 2px dashed #E2E8F0;
    border-radius: 16px;
    transition: all 0.3s ease;
    cursor: pointer;
    background: #ffffff;
    height: 110px;
}
.dark .upload-card { background: #1E293B; border-color: #334155; }
.upload-card:hover {
    border-color: var(--color-kpmg-default);
    background: rgba(0, 51, 141, 0.02);
    transform: translateY(-2px);
}
.upload-card.selected {
    border-style: solid;
    border-color: var(--color-kpmg-default);
    background: rgba(0, 51, 141, 0.05);
}

/* Progress Area */
.upload-progress-container {
    max-height: 0;
    overflow: hidden;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 0;
}
.upload-progress-container.active {
    max-height: 200px;
    opacity: 1;
    margin-top: 1.5rem;
}

.progress-bar-bg {
    height: 8px;
    background: #E2E8F0;
    border-radius: 10px;
    overflow: hidden;
}
.dark .progress-bar-bg { background: #1E293B; }

.progress-bar-fill {
    height: 100%;
    background: var(--color-kpmg-default);
    width: 0%;
    transition: width 0.3s ease;
}
.dark .progress-bar-fill { background: #60A5FA; }

/* Logs Collapsible */
.logs-content { max-height: 0; overflow: hidden; transition: max-height 0.5s cubic-bezier(0, 1, 0, 1); }
.logs-content.open { max-height: 1000px; transition: max-height 1s ease-in-out; }

.log-table { width: 100%; border-spacing: 0; }
.log-table th { 
    text-align: left; 
    padding: 12px; 
    font-size: 11px; 
    font-weight: 700;
    color: #64748B; 
    border-bottom: 1px solid #F1F5F9; 
    text-transform: none;
}
.dark .log-table th { border-bottom-color: #334155; color: #94A3B8; }
.log-table td { padding: 16px 12px; font-size: 12px; border-bottom: 1px solid #F1F5F9; }
.dark .log-table td { border-bottom-color: #334155; }

.report-link {
    color: var(--color-kpmg-default);
    text-decoration: none;
    transition: all 0.2s;
    cursor: pointer;
    font-weight: 700;
}
.dark .report-link { color: #60A5FA; }
.report-link:hover { text-decoration: underline; opacity: 0.8; }

.status-tag {
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.status-processed { background-color: #ECFDF5; color: #059669; }
.status-progress { background-color: #EFF6FF; color: #2563EB; }
.status-failed { background-color: #FEF2F2; color: #DC2626; }

.dark .status-processed { background-color: rgba(5, 150, 105, 0.1); color: #34D399; }
.dark .status-progress { background-color: rgba(37, 99, 235, 0.1); color: #60A5FA; }
.dark .status-failed { background-color: rgba(220, 38, 38, 0.1); color: #F87171; }

.table-border {
    border:1px solid black;
    border-collapse:collapse;
}

.sar-template-css {
        text-shadow: rgb(0 0 0 / 15%) 0 0 1px;
        font-size:1rem;

        font-family: Arial;
        font-weight: 400;
        line-height: 1.2;
        color: #424242;
    }
.sar-template-css .disabledDivContent {
	pointer-events: none;
	opacity: 0.4;
}
.sar-template-css .table-bordered {
    border: 1px solid #e9f1f1;
}
.sar-template-css .table td, .sar-template-css .table:not(.table-bordered) th {
    border-top: none;
}
.sar-template-css .table-bordered td, .sar-template-css .table-bordered th {
    border: 1px solid #e9f1f1;
}
.sar-template-css .table thead th {
    border-bottom: none;
    /* background: #fff; */
    padding-top: 15px;
    padding-bottom: 15px;
}
.sar-template-cssh1,
.sar-template-css h2,
.sar-template-css h3,
.sar-template-css h4,
.sar-template-css h5,
.sar-template-css h6,
.sar-template-css .h1,
.sar-template-css .h2,
.sar-template-css .h3,
.sar-template-css .h4,
.sar-template-css .h5,
.sar-template-css .h6
{
    font-family: Arial;
    font-weight: 400;
    line-height: 1.2;

    margin-bottom: .5rem;

    color: #424242;
}

.sar-template-css h1,
.sar-template-css .h1
{
    font-size: 2.572rem;
}

.sar-template-css h2,
.sar-template-css .h2
{
    font-size: 2.143rem;
}

.sar-template-css h3,
.sar-template-css .h3
{
    font-size: 1.715rem;
}

.sar-template-css h4,
.sar-template-css .h4
{
    font-size: 1.286rem;
}

.sar-template-css h5,
.sar-template-css .h5
{
    font-size: 1rem;
}

.sar-template-css h6,
.sar-template-css .h6
{
    font-size: .858rem;
}

/* Centered text */
.upper {
    position:absolute;
    top:25%;
    left:2%;
    transform:translateY(-50%);
}

.centered {
    position:absolute;
    top:75%;
    left:35%;
    transform:translate(-50%, -50%);
}

.image1 {
    position: relative;
    /*top: 0;*/
    /*left: 0;*/
}
.image2 {
    position: relative;
    height: 1056px;
    width: 816px;
    /*top: 30px;*/
    /*left: 30px;*/
}
.image3 {
    position: relative;
    z-index: 1;
    left: 16%;
    bottom: 950px;
    transform: translate(-50%, -50%);
    /*position: relative;
    left: 15%;
    bottom: 430px;
    transform: translate(-50%, -50%);
    margin-left:-0.5in;*/
    /*top: 0;*/
    /*left: 0;*/
}

/* #header_first_page {
    position: relative;
    width: 816px;
    height: 1056px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
} */

#header_first_page {
    position: relative;
    width: 816px;
    height: 1056px;
    overflow: hidden;
}

#header_first_page .upper p {
  line-height: 1.1 !important;
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}

.back_yellow {
    background: yellow;
}

 @keyframes gentle-pulse {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.15); opacity: 0.6; }
  }
  .animate-gentle-pulse {
      animation: gentle-pulse 2s infinite ease-in-out;
  }
  
#back-to-top {
    color: white;
    background-color: #ED2124;
}

#scroll-to-bottom {
    color: white;
    background-color: #ED2124;
}

.architecture-upload-wrapper {
  margin-bottom: 12px;
}

.architecture-upload-input {
  display: none;
}

.architecture-upload-label {
  display: inline-block;
  cursor: pointer;
  background-color: #00338d;
  color: #ffffff;
  border-radius: 6px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 500;
  margin-right: 10px;
}

.architecture-selected-files {
  font-size: 13px;
  color: #374151;
}

.architecture-upload-help {
  margin-top: 8px;
  font-size: 12px;
  color: #6b7280;
}

#toc_container {
  background: #f9f9f9;
  border: 1px solid #aaa;
  width: 100%;
  padding: 20px;
}

/* Contents heading */
#toc_container h2,
.toc_title {
  font-size: 26px;
  line-height: 1.2;
  color: #00338d;
  font-weight: 400;
}

/* Remove bullets */
#toc_container ul,
#toc_container li,
#toc_container ul li {
  list-style: none !important;
  margin: 0;
  padding: 0;
}

/* Main sections */
#toc_container > ul > li {
  margin-bottom: 28px;
}

#toc_container h3 {
  font-size: 24px;
  font-weight: 400;
  line-height: 1.3;
  color: #00338d;
  margin-left: 50px;
}

#toc_container h4 {
  font-size: 19.5px;
  font-weight: 400;
  color: #00338d;
  line-height: 1.3;
  margin-left: 40px;
}

/* Sub sections */
#toc_container ul ul {
  margin-left: 48px;
  margin-top: 8px;
}

#toc_container ul ul li {
  margin-bottom: 6px;
}

#toc_container ul ul a {
  font-size: 16px;
  line-height: 1.5;
  color: #00338d;
  text-decoration: none;
  font-weight: 400;
}

.segoe,
.segoe * {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Home page common global styles */
:root {
  --home-bg: #ffffff;
  --home-text: #0f1b3d;
  --home-muted: #64748b;
  --card-bg: #ffffff;
  --card-border: #eef0f6;
  --card-shadow: 0 8px 30px -12px rgba(60, 50, 140, 0.18);
  --card-shadow-hover: 0 20px 40px -14px rgba(90, 60, 200, 0.18);
}

.dark {
  --home-bg: #0f172b;
  --home-text: #e6eaf5;
  --home-muted: #94a3b8;
  --card-bg: #141a2e;
  --card-border: #232b45;
  --card-shadow: 0 8px 30px -12px rgba(0, 0, 0, 0.6);
  --card-shadow-hover: 0 20px 40px -14px rgba(0, 0, 0, 0.7);
}

.home-page {
  background: var(--home-bg);
  color: var(--home-text);
  transition:
    background-color 0.25s ease,
    color 0.25s ease;
}

.action-card {
  position: relative;
  isolation: isolate;
  min-width: 0;
  border: 1px solid var(--card-border);
  border-radius: 20px;
  background: var(--card-bg);
  box-shadow: var(--card-shadow);
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.action-card::before {
  position: absolute;
  z-index: -1;
  inset: 14px 10px -10px;
  border-radius: 24px;
  background: linear-gradient(
    90deg,
    #4f7cff 0%,
    #8b5cf6 50%,
    #ec4899 100%
  );
  content: "";
  filter: blur(22px);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.action-card::after {
  position: absolute;
  z-index: -1;
  inset: 0;
  border-radius: inherit;
  background: var(--card-bg);
  content: "";
}

a.action-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--card-shadow-hover);
}

a.action-card:hover::before {
  opacity: 0.55;
}

.card-icon {
  display: flex;
  width: 52px;
  height: 52px;
  flex: none;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  background: var(--accent);
  color: #ffffff;
  box-shadow: 0 8px 18px -6px var(--accent-shadow);
}

.accent-threat {
  --accent: #be185d;
  --accent-shadow: rgba(190, 24, 93, 0.45);
  --accent-text: #be185d;
}

.accent-assess {
  --accent: #7c3aed;
  --accent-shadow: rgba(124, 58, 237, 0.45);
  --accent-text: #7c3aed;
}

.accent-track {
  --accent: #1e3a8a;
  --accent-shadow: rgba(30, 58, 138, 0.45);
  --accent-text: #1e3a8a;
}

.accent-reports {
  --accent: #b45309;
  --accent-shadow: rgba(180, 83, 9, 0.45);
  --accent-text: #b45309;
}

.dark .accent-threat {
  --accent-text: #f472b6;
}

.dark .accent-assess {
  --accent-text: #a78bfa;
}

.dark .accent-track {
  --accent: #2e4fb8;
  --accent-text: #7da2ff;
}

.dark .accent-reports {
  --accent-text: #fbbf24;
}

.card-desc {
  color: var(--home-muted);
}

.card-link {
  color: var(--accent-text);
}

a.action-card:hover .card-link {
  gap: 12px;
}

.gradient-text {
  display: inline-block;
  background: linear-gradient(
    90deg,
    #3b6cf6 0%,
    #8b5cf6 50%,
    #ec4899 100%
  );
  background-clip: text;
  color: transparent;
  -webkit-background-clip: text;
}

.dark .gradient-text {
  background-image: linear-gradient(
    90deg,
    #6b93ff 0%,
    #a78bfa 50%,
    #f472b6 100%
  );
}

