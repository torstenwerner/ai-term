/**
 * Is the current prompt type a YouTube prompt type?
 */
export function isYoutubePrompt(type) {
    return type === 'YOUTUBE_EN' || type === 'YOUTUBE_DE';
}

const YOUTUBE_URL_PATTERN = /^https:\/\/(www\.)?youtu/;

/**
 * Is the given prompt a valid YouTube URL?
 */
export function isValidYoutubeUrl(prompt) {
    return prompt.match(YOUTUBE_URL_PATTERN);
}

