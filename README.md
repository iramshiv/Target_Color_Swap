# Target_Color_Swap

python testswap.py --image /input-image-path/ --output /output-directory-to-save/ --target_rgb 37 88 128

In between the exceution, there will be a palette with the cluster of colors. Input an target cluster you wish. 
    
    *Note: Clusters start from '0'.

Default cluster size is 2 to 7 but you can change that with 'mink' and 'maxk' values.

You can also play with 'shades_range' (for darker side of the cluster) and 'tint_range' (for lighter side of the cluster) arguments, if your target cluster are not properly replaced.

'target_rgb' takes RGB value of a color, you like to see.
 

## Other Arguments
   
   --mink: default is 2. Minimum cluster
   
   --maxk: default is 7. Maximum Cluster
   
   --shades_range: default is 5. Finds 5 next nearest shades(dark) to replace.
   
   --tint_range: default is 5. Finds 5 next nearest tint(light) to replace.
    
<p float="left">
    <img src="3a.jpg" title="Source Image"  width="512" height="512">
    <img src="result.jpg" title="Target Image" width="512" height="512">
</p>

  - Required library : PIL, Python, matplotlib, cv2, numpy, pandas, sklearn
