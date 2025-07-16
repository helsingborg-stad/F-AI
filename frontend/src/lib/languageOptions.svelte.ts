// import { getLocale, type Locale, setLocale } from '../paraglide/runtime.js'
// import type { ILanguage, ILanguageOptions } from '$lib/types.js'
//
// export const SUPPORTED_LANGUAGES: ILanguage[] = [
//   { code: 'en', name: 'English' },
//   { code: 'sv', name: 'Svenska' },
// ]
//
// export let currentLanguage = $state(getLocale())
//
// export function getLanguageByCode(code: string): ILanguage | undefined {
//   return SUPPORTED_LANGUAGES.find((language) => language.code === code)
// }
//
// // export function getCurrentLanguage(): ILanguage | undefined {
// //   const currentLocale = getLocale()
// //   return getLanguageByCode(currentLocale)
// // }
//
// export function createLanguageOptions(): ILanguageOptions {
//   let selectedLanguage = $state(getLocale())
//
//   return {
//     languages: SUPPORTED_LANGUAGES,
//     get selectedLanguage() {
//       return selectedLanguage
//     },
//     setLanguage: (languageCode: string) => {
//       const isSupported = SUPPORTED_LANGUAGES.some(
//         (language) => language.code === languageCode,
//       )
//
//       if (!isSupported) {
//         console.warn(`Language ${languageCode} is not supported`)
//         return
//       }
//
//       selectedLanguage = languageCode as Locale
//       setLocale(selectedLanguage)
//     },
//   }
// }
