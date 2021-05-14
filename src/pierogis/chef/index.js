import { initDropArea } from "./input.js";

async function loadPyodideAndPackages(){
    await loadPyodide({ indexURL : "https://cdn.jsdelivr.net/pyodide/v0.17.0/full/" });
    await pyodide.loadPackage('numpy');
    await pyodide.loadPackage('pillow');
    await pyodide.loadPackage('imageio');
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install('https://files.pythonhosted.org/packages/ad/0c/f7308a3dca51bc2fee95dc8b7f3b6faa52f03b05373a390b302dddaa6aa8/pierogis-0.4.0-cp38-cp38-macosx_11_0_arm64.whl')
    `)
}

let pyodideReadyPromise = loadPyodideAndPackages();

async function cook(e) {
    let upperSlider = document.getElementById("upper-slider");
    let lowerSlider = document.getElementById("lower-slider");
    let thresholdString = `Threshold(upper_threshold=${upperSlider.value}, lower_threshold=${lowerSlider.value})`

    let ingredientOptions = document.getElementsByName('ingredient')
    let ingredientString;
    let seasonString;

    for (let i = 0; i < ingredientOptions.length; i++) {
        if (ingredientOptions[i].checked) {
            switch (ingredientOptions[i].value) {
                case 'sort':
                    ingredientString = "Sort()";
                    seasonString = "ingredient.season(" + thresholdString + ")"
                    break;
                case 'threshold':
                    ingredientString = thresholdString;
                    seasonString = ""
                    break;
                case 'quantize':
                    ingredientString = "Quantize(colors=['000000', 'ffffff'])";
                    break;
                default:
                    // code block
            }
        }
    }

    globalThis.input_image_bytes_array = e.target.result;

    return await pyodide.runPythonAsync(`
        import io
        import base64

        from pierogis.ingredients import SpatialQuantize, Pierogi, Sort, Threshold, Quantize

        from js import input_image_bytes_array

        bytes = io.BytesIO(input_image_bytes_array.to_py())
        pierogi = Pierogi.from_path(bytes)

        ingredient = ${ingredientString}
        ${seasonString}

        cooked_pixels = ingredient.cook(pierogi.pixels)

        buf = io.BytesIO()
        Pierogi(pixels=cooked_pixels).image.save(buf, format='PNG')
        buf.seek(0)
        'data:image/png;base64,' + base64.b64encode(buf.read()).decode('UTF-8')
    `);
}

async function cookHandler(){
    await pyodideReadyPromise;

    let imageInput = document.getElementById("image-input");
    var file = imageInput.files[0];

    const reader = new FileReader();
    reader.onload = async e => {
        cook(e).then(function (imageString) {
            document.getElementById("image").src = imageString;
        }).catch(function (error) {
            console.log("cook failed: ", error);
        });
    }

    reader.readAsArrayBuffer(file);
}

function init() {
    let upperSlider = document.getElementById("upper-slider");
    let upperDisplay = document.getElementById("upper-display");
    let lowerSlider = document.getElementById("lower-slider");
    let lowerDisplay = document.getElementById("lower-display");

    upperDisplay.innerHTML = upperSlider.value;
    lowerDisplay.innerHTML = lowerSlider.value;

    lowerSlider.oninput = function() {
        lowerDisplay.innerHTML = this.value;
    }
    upperSlider.oninput = function() {
        upperDisplay.innerHTML = this.value;
    }

    let cookButton = document.getElementById("cook-button");

    cookButton.onclick = cookHandler;
}

document.addEventListener('readystatechange', function() {
    if (document.readyState === "complete") {
        init();
        initDropArea();
    }
});
