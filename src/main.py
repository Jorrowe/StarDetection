import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import simple_norm
from photutils.detection import DAOStarFinder
from astropy.stats import mad_std

# Load image data
image_file = 'MAST_2024-07-11T0203/JWST/jw02731-o001_t017_nircam_clear-f187n/jw02731-o001_t017_nircam_clear-f187n_i2d.fits'
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
# Plot detected stars
plt.imshow(image_data, norm=norm, cmap='gray')
plt.xlim(0, 14340)
plt.ylim(0, 8582)
plt.title('Orignal image')
plt.show()
