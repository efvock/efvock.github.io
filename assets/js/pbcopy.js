document.getElementById("copyBtn").addEventListener("click", async () => {
    let msg;
    let status;
    let targetData;
    try {
        const siteData = window.jekyllSiteData;
        const urlParams = new URLSearchParams(window.location.search);
        const dataKey = urlParams.get("data");
        const json = urlParams.get("json");
        if (!dataKey) {
            status = "default"
        } else {
            targetData = siteData[dataKey];
            if (targetData === undefined) {
                status = "ng";
            } else {
                status = "ok";
            }
        }
        if (status === "ng") {
            msg = `${dataKey}: not found`;
        } else if (status === "ok") {
            msg = `${dataKey}: copied`;
        } else {
            msg = "{} copied";  //
        }
        alert(msg);
        if (status === "ng") {
            return;
        }
        if (!json) {
            targetData ||= "";
            await navigator.clipboard.writeText(targetData);
            return;
        }
        const formattedJson =
            status === "default"
                ? "{}"
                : JSON.stringify(targetData, null, 2)
            ;
        await navigator.clipboard.writeText(formattedJson);
    } catch (error) {
        alert(error);
    }
});
