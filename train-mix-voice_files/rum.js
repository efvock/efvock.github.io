let zoneList = [];
let currentZoneIndex = 0;
let testId = null;
const CONCURRENCY = 3;

// Fisher–Yates shuffle
function shuffle(array) {
    let m = array.length, t, i;
    while (m) {
        i = Math.floor(Math.random() * m--);
        t = array[m];
        array[m] = array[i];
        array[i] = t;
    }
    return array;
}

// Pull the next zone (or null when done)
function getNextZone() {
    return currentZoneIndex < zoneList.length
        ? zoneList[currentZoneIndex++]
        : null;
}

// One full chain: grab a zone → run it → repeat until empty
async function launchChain() {
    let zone;
    while ((zone = getNextZone())) {
        await runNextTest(zone);
    }
    //console.log('➤ chain complete');
}

// The “hello” gate → only once that resolves do we start our 3 chains
async function runMetricsTest() {
    try {
        // 1) register
        const regRes = await fetch('https://metrics-bunny.net/test/register');
        if (!regRes.ok) throw new Error(`register failed (${regRes.status})`);
        const data = await regRes.json();
        //console.log('✅ register response:', data);

        testId = data.uniqueId;
        // defend against a missing/empty zoneList
        const rawZones = data.zoneList;
        if (!Array.isArray(rawZones) || rawZones.length === 0) {
            //console.error('❌ no zones in register response, aborting');
            return;
        }

        // 2) shuffle and seed
        zoneList = shuffle(rawZones.slice());
        //console.log('🔀 shuffled zones:', zoneList);

        // 3) hello handshake
        const helloUrl = `https://${testId}.metrics-bunny.net/test/hello`;
        //console.log('👋 sending hello to:', helloUrl);
        const helloRes = await fetch(helloUrl);
        if (!helloRes.ok) throw new Error(`hello failed (${helloRes.status})`);
        //console.log('👍 handshake OK');

        // 4) reset index & fire up concurrent chains
        currentZoneIndex = 0;
        for (let i = 0; i < CONCURRENCY; i++) {
            launchChain();
        }
    } catch (err) {
        //console.error('runMetricsTest error:', err);
    }
}

// Run one latency test + report (with testId)
async function runNextTest(zone) {
    const zoneCode = zone.toLowerCase();
    //console.log(`→ testing zone ${zoneCode}:`, url);
    
    try {

        var url = `https://edgezone-${zoneCode}.bunnyinfra.net/500b.jpg?s=${Date.now()}`;
        await fetch(url);
        const start = Date.now();

        url = `https://edgezone-${zoneCode}.bunnyinfra.net/500b.jpg?s=a${Date.now()}`;
        await fetch(url);
        const latency = Date.now() - start;

        const reportUrl =
            `https://metrics-bunny.net/test/trackperformance` +
            `?zone=${zoneCode}&latency=${latency}&testId=${testId}`;
        //console.log(`→ reporting ${zoneCode}:`, reportUrl);

        await fetch(reportUrl);
    } catch (err) {
        //console.error(`runNextTest error [${zoneCode}]:`, err);
    }
}

runMetricsTest();