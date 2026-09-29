const DICTIONARY_FILE = "dictionary_stage14_grouped.csv";
const REVERSE_INDEX_FILE = "dictionary_stage18_reverse_index.json";

let rows = [];
let reverseIndex = {};

const searchInput = document.getElementById("searchInput");
const searchMode = document.getElementById("searchMode");
const resultsBox = document.getElementById("results");
const statusText = document.getElementById("dictionaryStatus");

/* ============================================================
   SPLASH SCREEN
   ============================================================ */

function hideSplashScreen() {
    const splash = document.getElementById("splashScreen");
    if (splash) {
        splash.classList.add("fade-out");
        setTimeout(() => splash.remove(), 600);
    }
}

/* ============================================================
   CSV PARSER
   ============================================================ */

function parseCSV(text) {
    const records = [];
    let row = [];
    let field = "";
    let insideQuotes = false;

    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        const next = text[i + 1];

        if (char === '"') {
            if (insideQuotes && next === '"') {
                field += '"';
                i++;
            } else {
                insideQuotes = !insideQuotes;
            }
        } else if (char === "," && !insideQuotes) {
            row.push(field);
            field = "";
        } else if ((char === "\n" || char === "\r") && !insideQuotes) {
            if (char === "\r" && next === "\n") {
                i++;
            }
            row.push(field);
            field = "";
            if (row.length > 1 || row[0] !== "") {
                records.push(row);
            }
            row = [];
        } else {
            field += char;
        }
    }

    if (field !== "" || row.length > 0) {
        row.push(field);
        records.push(row);
    }

    if (records.length === 0) return [];

    const headers = records[0].map(h => h.trim());

    return records.slice(1).map(record => {
        const object = {};
        headers.forEach((header, index) => {
            object[header] = record[index] || "";
        });
        return object;
    });
}

/* ============================================================
   LOAD DICTIONARY
   ============================================================ */

async function loadDictionary() {
    const splashDelay = new Promise(resolve => setTimeout(resolve, 1800));

    try {
        if (statusText) statusText.textContent = "Loading dictionary...";

        const dictionaryResponse = await fetch(DICTIONARY_FILE);
        if (!dictionaryResponse.ok) {
            throw new Error("Could not load dictionary CSV");
        }

        const csvText = await dictionaryResponse.text();
        rows = parseCSV(csvText);

        const reverseResponse = await fetch(REVERSE_INDEX_FILE);
        if (reverseResponse.ok) {
            reverseIndex = await reverseResponse.json();
        }

        if (statusText) {
            statusText.textContent = `${rows.length.toLocaleString()} dictionary headwords loaded`;
        }

    } catch (error) {
        console.error(error);
        if (statusText) statusText.textContent = "Dictionary loading failed";
        resultsBox.innerHTML = `
            <div class="no-results">
                Could not load dictionary data.<br>
                ${escapeHTML(error.message)}
            </div>
        `;
    } finally {
        await splashDelay;
        hideSplashScreen();
    }
}

/* ============================================================
   ENGLISH SEARCH
   ============================================================ */

function searchEnglish(query) {
    const exact = rows.filter(row =>
        (row.lookup_headword || "").trim().toLowerCase() === query
    );

    if (exact.length > 0) return exact;

    return rows.filter(row =>
        (row.lookup_headword || "").toLowerCase().includes(query)
    );
}

/* ============================================================
   SINDHI SEARCH
   ============================================================ */

function searchSindhi(query) {
    const results = [];

    if (reverseIndex && Object.keys(reverseIndex).length > 0) {
        const englishWords = reverseIndex[query];
        if (Array.isArray(englishWords) && englishWords.length > 0) {
            const englishSet = new Set(englishWords);
            for (const row of rows) {
                const english = (row.english_headword || "").trim();
                if (englishSet.has(english)) {
                    results.push(row);
                }
            }
            if (results.length > 0) return results;
        }
    }

    return rows.filter(row => {
        const sindhi = (row.sindhi_translations || "");
        return sindhi.includes(query);
    });
}

/* ============================================================
   SEARCH LOGIC
   ============================================================ */

function performSearch() {
    const query = searchInput.value.trim().toLowerCase();
    resultsBox.innerHTML = "";

    if (!query) {
        if (statusText) {
            statusText.textContent = `${rows.length.toLocaleString()} dictionary headwords`;
        }
        return;
    }

    let results;
    if (searchMode.value === "english") {
        results = searchEnglish(query);
    } else {
        results = searchSindhi(query);
    }

    displayResults(results);
}

/* ============================================================
   DISPLAY RESULTS
   ============================================================ */

function displayResults(results) {
    if (!results || results.length === 0) {
        resultsBox.innerHTML = `
            <div class="no-results">
                No matching entry found.
            </div>
        `;
        if (statusText) statusText.textContent = "No results";
        return;
    }

    const limitedResults = results.slice(0, 50);

    for (const row of limitedResults) {
        const english = (row.english_headword || "").trim();
        const sindhi = (row.sindhi_translations || "").trim();

        const result = document.createElement("div");
        result.className = "result";

        const englishElement = document.createElement("div");
        englishElement.className = "english";
        englishElement.textContent = english;

        const sindhiElement = document.createElement("div");
        sindhiElement.className = "sindhi";
        sindhiElement.textContent = sindhi;

        result.appendChild(englishElement);
        result.appendChild(sindhiElement);
        resultsBox.appendChild(result);
    }

    if (results.length > 50) {
        const more = document.createElement("div");
        more.className = "no-results";
        more.textContent = `... and ${(results.length - 50).toLocaleString()} more matches.`;
        resultsBox.appendChild(more);
    }

    if (statusText) {
        statusText.textContent = `${results.length.toLocaleString()} matches`;
    }
}

/* ============================================================
   MODE CHANGE & INPUT EVENTS
   ============================================================ */

searchMode.addEventListener("change", () => {
    if (searchMode.value === "english") {
        searchInput.placeholder = "Search English word...";
    } else {
        searchInput.placeholder = "سنڌي لفظ ڳوليو...";
    }
    searchInput.value = "";
    resultsBox.innerHTML = "";
});

searchInput.addEventListener("input", performSearch);

searchInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        performSearch();
    }
});

/* ============================================================
   HTML SAFETY
   ============================================================ */

function escapeHTML(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

/* ============================================================
   START
   ============================================================ */

loadDictionary();
