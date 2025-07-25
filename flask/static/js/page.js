const audio = new Audio();
let isPaused = false;
let isStopped = false;
let isReading = false;

let lines = [];

const pageInput = document.getElementById("pageInput");
const pageCount = document.getElementById("pageCount");

const readPageBtn = document.getElementById("readPageBtn");
const pausePageBtn = document.getElementById("pausePageBtn");
const stopPageBtn = document.getElementById("stopPageBtn");

async function flipPage(direction) {
  try {
    const params = new URLSearchParams(window.location.search);

    const response = await fetch('/book/flip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: params.get("id"), d: direction })
    });
    console.log("Submitted:", response);
    
    location.reload();
  } catch (err) {
    console.error("Error:", err);
  }
}

async function playWav(audioUrl) {
  try {
    audio.src = audioUrl;

    await new Promise((resolve, reject) => {
      audio.onended = () => {
        URL.revokeObjectURL(audio.src);
        resolve();
      };
      audio.onerror = (e) => reject(e);
      audio.play().catch(reject); // Play might reject if autoplay is blocked
    });
  }
  catch (error) {
    console.error("playWav failed");
  }
}

async function getWav(text) {
  try {
    const response = await fetch('/piper/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: text })
    });

    if (!response.ok) throw new Error("Failed to fetch WAV file");

    const blob = await response.blob();
    return URL.createObjectURL(blob);

  } catch (error) {
    console.error('Fetch/play error:', error);
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function parseText() {
  const pageContainers = document.querySelectorAll('[id^="pf"]');

  for (const container of pageContainers) {
    const firstLayer = container.querySelector("div");
    const secondLayer = firstLayer.querySelector("div");

    lines = Array.from(secondLayer.querySelectorAll('div'));
    return lines;
  }
}

function processText() {
  let fullText = '';
  const lineOffsets = [];
  lines.forEach((line, i) => {
    line = line.innerText;
    lineOffsets.push({ start: fullText.length, end: fullText.length + line.length, index: i });
    fullText += line + ' ';
  });

  // Regex to match sentences (includes last chunk even without punctuation)
  const sentenceRegex = /[^.!?]+[.!?]+|\s*[^.!?]+$/g;
  const matches = [];
  let match;
  while ((match = sentenceRegex.exec(fullText)) !== null) {
    matches.push({
      0: match[0],
      index: match.index
    });
  }

  // Result: { text: string, lines: number[] }
  const sentences = matches.map(match => {
    const sentence = match[0].trim();
    const start = match.index;
    const end = start + sentence.length;

    // Find which lines this sentence overlaps
    const linesUsed = lineOffsets
      .filter(line => !(line.end < start || line.start > end))
      .map(line => line.index);

    return { text: sentence, lines: linesUsed };
  });

  return sentences;

  // Output example
  /*
  sentences.forEach((s, i) => {
    console.log(s);
  });
  */
}

let wrapperDiv = null;
function highlightElements (indexes, active) {
  // Remove previous wrapper
  if (wrapperDiv) {
    wrapperDiv.remove();
    wrapperDiv = null;
  }

  if (!active || indexes.length === 0) return;

  // Get the DOM elements representing lines
  const targetElems = indexes.map(i => lines[i]);

  // Get bounding box extremes
  const rects = targetElems.map(el => el.getBoundingClientRect());

  const minTop = Math.min(...rects.map(r => r.top));
  const maxBottom = Math.max(...rects.map(r => r.bottom));
  const minLeft = Math.min(...rects.map(r => r.left));
  const maxRight = Math.max(...rects.map(r => r.right));

  // Account for scroll offset
  const scrollY = window.scrollY;
  const scrollX = window.scrollX;

  // Create wrapper
  const PADDING = 10;
  wrapperDiv = document.createElement('div');
  wrapperDiv.style.position = 'absolute';
  wrapperDiv.style.border = '2px solid black';
  wrapperDiv.style.borderRadius = '8px';
  wrapperDiv.style.pointerEvents = 'none';
  wrapperDiv.style.zIndex = '9999';
  wrapperDiv.style.top = (minTop + scrollY - PADDING) + 'px';
  wrapperDiv.style.left = (minLeft + scrollX - PADDING) + 'px';
  wrapperDiv.style.width = (maxRight - minLeft + PADDING * 2) + 'px';
  wrapperDiv.style.height = (maxBottom - minTop + PADDING * 2) + 'px';

  // Add to body
  document.body.appendChild(wrapperDiv);
}

readPageBtn.addEventListener('click', async () => {
  readPageBtn.disabled = true;
  pausePageBtn.disabled = false;
  stopPageBtn.disabled = false;

  if (isPaused) {
    audio.play();
  } 
  else {
    isStopped = false;

    const elements = await parseText();
    const sentences = processText();

    for (const sentence of sentences) {
      if (isStopped){
        break;
      }
      console.log(sentence);

      highlightElements(sentence.lines, true);

      const audioUrl = await getWav(sentence.text);
      await playWav(audioUrl);

      highlightElements(sentence.lines, false);

    }
  }
  isPaused = false;

  readPageBtn.disabled = false;
});

pausePageBtn.addEventListener('click', async () => {
  audio.pause();
  isPaused = true;

  readPageBtn.disabled = false;
  pausePageBtn.disabled = true;
  stopPageBtn.disabled = false;
});

stopPageBtn.addEventListener('click', async () => {
  audio.pause();
  highlightElements([], false);

  isStopped = true;
  isPaused = false;

  readPageBtn.disabled = false;
  pausePageBtn.disabled = true;
  stopPageBtn.disabled = true;
});

pageInput.addEventListener('input', function (e) {
  this.value = this.value.replace(/[^0-9]/g, '');
});

pageInput.addEventListener('keydown', function (e) {
  if (event.key === 'Enter') {
    const currentPage = parseInt(e.target.value);
    
    if (currentPage <= parseInt(pageCount.innerText) && currentPage > 0){
      flipPage(currentPage);
    }
    else {
      pageInput.value = "";
    }
  }
})
