# tiny-tools

### introduction
Here are tiny tools to improve efficiency. I will introduce these tools below. And you can get more details in "README.md" in subfolders.

### bookmarks counter
When there are too many bookmarks, how to count bookmarks? Export bookmarks from chrome, replace `bookmarks.html` with your bookmarks file and run `python3 bookmarks_counter.py`. And then you will know it.

Possible that you need to install some dependencies like below to run it:
```bash
pip3 install beautifulsoup4
```

### code_template
##### create_package
Create a package according to template. You can edit it to make it more suitable for your situation.

### data_process
##### fast_fourier_transform
##### json_tree
visualize json as a tree.
##### normal_distribution
Read the values from file, skip zero values if necessary. Normalize the data and calculate the normal distribution parameters. At last, plot values.
##### yaml
Read, process and save file in format yaml. Comments in original file will be remained.

### deduplication
In some cases, we may store some same files or similiar pictures. This folder contains tools to help you deal with them.
##### 

### image
##### svg3png
convert image from `webp` to `png`.
##### webp2png
convert image from `webp` to `png`.

### time
##### timer

### visualize
This folder contains tools that visualize data(distributed in 2D plane) with charts.

### qr_code
According to your domain/site, generate QR code. You can also generate code for something else.
