# flake8: noqa: W605

SORT_TABLE_BY_COLUMN_JAVASCRIPT = """
<script>
function sortTableByColumn(tableId, columnIndex) {
    const table = document.getElementById(tableId);
    let rows = Array.from(table.rows).slice(1); // Skip header row
    let dir = table.getAttribute("data-sort-dir") === "asc" ? "desc" : "asc";
    table.setAttribute("data-sort-dir", dir);

    // Get a non-empty sample value from the column to detect type
    let sampleValue = "";
    for (const row of rows) {
        const cell = row.cells[columnIndex];
        if (cell && cell.textContent.trim()) {
            sampleValue = cell.textContent.trim();
            break;
        }
    }

    const type = detectType(sampleValue);

    rows.sort((a, b) => {
        let x = a.cells[columnIndex]?.textContent.trim() || "";
        let y = b.cells[columnIndex]?.textContent.trim() || "";

        return compareValues(x, y, type, dir);
    });

    // Reattach sorted rows
    for (const row of rows) {
        table.tBodies[0].appendChild(row);
    }

    // Utility: detect data type
    function detectType(val) {
        const cleaned = val.replace(/,/g, '');
        if (!isNaN(parseFloat(cleaned)) && isFinite(cleaned)) return "number";
        const datePattern = /^(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})$/;
        if (datePattern.test(val.trim()) && !isNaN(Date.parse(val))) return "date";
        return "text";
    }

    // Utility: compare values by type
    function compareValues(a, b, type, direction) {
        let result = 0;

        if (type === "number") {
            const numA = parseFloat(a.replace(/[^\d.-]/g, '')) || 0;
            const numB = parseFloat(b.replace(/[^\d.-]/g, '')) || 0;
            result = numA - numB;
        } else if (type === "date") {
            result = new Date(a).getTime() - new Date(b).getTime();
        } else {
            result = a.localeCompare(b);
        }

        return direction === "asc" ? result : -result;
    }
}
</script>
"""
