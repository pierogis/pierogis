use ndarray::Array;

fn quantize(array: ArrayView<'_, u8>) -> Vec<u8> {
    let width = array.width;
    let height = array.height;

    use rscolorq::{color::Rgb, Matrix2d, Params};

    // Create the output buffer and quantized palette index buffer
    let mut imgbuf = Vec::with_capacity(width * height * 3);
    let mut matrix = Matrix2d::new(width, height);

    // Build the quantization parameters, verify if accepting user input
    let mut conditions = Params::new();
    conditions.palette_size(palette_size);
    conditions.verify_parameters()?;

    // Convert the input image buffer from Rgb<u8> to Rgb<f64>
    let image = Matrix2d::from_vec(
        array.iter()
            .map(|&c| Rgb {
                red: c[0] as f64 / 255.0,
                green: c[1] as f64 / 255.0,
                blue: c[2] as f64 / 255.0,
            })
            .collect(),
        width,
        height,
    );

    let mut palette = Vec::with_capacity(palette_size as usize);

    rscolorq::spatial_color_quant(&image, &mut matrix, &mut palette, &conditions);

    // Convert the Rgb<f64> palette to Rgb<u8>
    let palette = palette
        .iter()
        .map(|&c| {
            let color = 255.0 * c;
            [
                color.red.round() as u8,
                color.green.round() as u8,
                color.blue.round() as u8,
            ]
        })
        .collect::<Vec<[u8; 3]>>();

    // Create the final image by color lookup from the palette
    matrix.iter().for_each(|&c| {
        imgbuf.extend_from_slice(&*palette.get(c as usize).unwrap());
    });
    imgbuf
}