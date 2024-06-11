export function matchCurrentPath(
    givenPathWithQuery: string,
    currentPath: string,
    currentQueryParams: URLSearchParams,
    placeholder: string = '*',
    greedy: boolean = false
): boolean {
    function preparePath(path: string): { basePath: string, queryParams: URLSearchParams } {
        const url = new URL(path, 'http://example.com');  // Use arbitrary base URL for parsing
        return {
            basePath: url.pathname.replace(/\/$/, ''),
            queryParams: new URLSearchParams(url.search)
        };
    }

    function createRegexPattern(path: string): string {
        if (path.includes('*')) {
            const regexSafePath = path.replace(/[\-\[\]\/\{\}\(\)\+\?\.\\\^\$\|]/g, "\\$&");  // Escape regex characters
            return regexSafePath.replace(/\*/g, greedy ? '(.*)' : '([^/]*)');  // Replace * with regex groups
        }
        return path;
    }

    const given = preparePath(givenPathWithQuery);

    const regex = new RegExp(`^${createRegexPattern(given.basePath)}$`);  // Match entire path exactly
    const isBasePathMatch = regex.test(currentPath);

    let isQueryParamMatch = true;
    given.queryParams.forEach((value, key) => {
        if (!currentQueryParams.has(key) || currentQueryParams.get(key) !== value) {
            isQueryParamMatch = false;
        }
    });

    return isBasePathMatch && isQueryParamMatch;
}