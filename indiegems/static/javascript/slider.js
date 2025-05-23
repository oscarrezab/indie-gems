const sliders = [
    document.getElementById("bpm_slider"),
    document.getElementById("key_slider"),
    document.getElementById("lyrics_slider"),
];

const values = [
    document.getElementById("value1"),
    document.getElementById("value2"),
    document.getElementById("value3"),
];

function updateValues() {
    sliders.forEach((slider, i) => {
        values[i].textContent = parseFloat(slider.value).toFixed(2);
    });
}

function onSliderInput(changedIndex) {
    const total = 1.0;
    const changedValue = parseFloat(sliders[changedIndex].value);

    // Get the other two indices
    const otherIndices = [0, 1, 2].filter(i => i !== changedIndex);

    let raw0 = sliders[otherIndices[0]].valueAsNumber;
    let raw1 = sliders[otherIndices[1]].valueAsNumber;

    let remaining = total - changedValue;

    // Avoid division by zero
    if (raw0 + raw1 === 0) {
        raw0 = raw1 = 0.5;
    }

    const ratio0 = raw0 / (raw0 + raw1);
    const ratio1 = raw1 / (raw0 + raw1);

    // Calculate unrounded new values
    let val0 = remaining * ratio0;
    let val1 = remaining * ratio1;

    // Round to 2 decimals
    let rounded0 = Math.round(val0 * 100) / 100;
    let rounded1 = Math.round(val1 * 100) / 100;

    // Fix rounding drift by adjusting one value and avoid value sums greater than 1
    let sum = changedValue + rounded0 + rounded1;
    let error = Math.round((total - sum) * 100) / 100;

    // Apply correction to the slider with the larger remaining portion
    if (error !== 0) {
        if (rounded0 >= rounded1) {
            rounded0 += error;
        } else {
            rounded1 += error;
        }
    }

    // Set values
    sliders[otherIndices[0]].value = rounded0.toFixed(2);
    sliders[otherIndices[1]].value = rounded1.toFixed(2);

    updateValues();
}

// Initial update for spans based on slider values already in the DOM
window.addEventListener("DOMContentLoaded", updateValues);

sliders.forEach((slider, index) => {
    slider.addEventListener("input", () => onSliderInput(index));
});
