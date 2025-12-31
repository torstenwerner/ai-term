<script>
    export let type;
    export let disabled = false;
    export let onChange;

    function description() {
        switch (type) {
            case 'DICTIONARY_EN':
                return 'A dictionary of English language.';
            case 'ENCYCLOPEDIA_EN':
                return 'An encyclopedia answering in English language.';
            case 'ENCYCLOPEDIA_DE':
                return 'An encyclopedia answering in German language.'
            case 'YOUTUBE_EN':
                return 'A YouTube summarizer in English language.'
            case 'YOUTUBE_DE':
                return 'A YouTube summarizer in German language.'
        }
        return '';
    }
</script>

<select
        bind:value={type}
        on:change={onChange}
        disabled={disabled}
>
    <option value="DICTIONARY_EN">English Dictionary</option>
    <option value="ENCYCLOPEDIA_EN">English Encyclopedia</option>
    <option value="ENCYCLOPEDIA_DE">German Encyclopedia</option>
    <option value="YOUTUBE_EN">English YouTube</option>
    <option value="YOUTUBE_DE">German YouTube</option>
</select>
<em>{description()}</em>

<style>
    select {
        padding: 0.5rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
        margin-right: 1rem;
        margin-bottom: 1rem;
        width: max(250px, 33%);
    }

    @media (prefers-color-scheme: dark) {
        select {
            background-color: #1a1a1a;
            color: rgba(255, 255, 255, 0.87);
            border-color: #555;
        }
    }
</style>
