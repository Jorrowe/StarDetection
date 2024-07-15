import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import simple_norm
from photutils.detection import DAOStarFinder
from astropy.stats import mad_std
from photutils.aperture import CircularAperture

# Load image data
image_file = "INPUT_FITS_DIRECTORY"
hdu_list = fits.open(image_file)

# Check the structure of the FITS file
print(f"Number of HDUs: {len(hdu_list)}")
for i, hdu in enumerate(hdu_list):
    print(f"HDU {i}: {hdu}")

# Assuming the image data is in the primary HDU or first extension
image_data = hdu_list[0].data
if image_data is None or image_data.ndim != 2:
    image_data = hdu_list[1].data  # Try the first extension

# Ensure the data is in a proper numeric format
image_data = np.array(image_data, dtype=np.float64)

# Handle NaNs and infinities
image_data[np.isnan(image_data)] = 0
image_data[np.isinf(image_data)] = 0

# Check the shape of the data
print(f"Image data shape: {image_data.shape}")

# Normalize and display image
norm = simple_norm(image_data, 'linear', percent=99)

# Star detection
bkg_sigma = mad_std(image_data)
daofind = DAOStarFinder(fwhm=3.0, threshold=5.*bkg_sigma)
sources = daofind(image_data)

# Plot detected stars
positions = (sources['xcentroid'], sources['ycentroid'])
plt.imshow(image_data, norm=norm, cmap='gray')
plt.scatter(positions[0], positions[1], s=30, edgecolor='red', facecolor='none')
plt.title('Detected Stars')
plt.show()
