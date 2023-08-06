function _addDelta(inputId, delta) {
    const input = document.getElementById(inputId);
    input.value = Number(input.value) + Number(delta);
}
