python setup.py install
cargo install --path ../rscolorq
rscolorq -i demo/gnome.jpg -o output.png -n 16 -s 0 --iters 3 --repeats 3
pierogis quantize demo/gnome.jpg -n 16 -i 3 -r 3
