# Install
```
module purge all
module load python/anaconda3.6
conda create --prefix /projects/a9009/sbc538/documentation/documentation-env -c conda-forge django-extensions django python=3.8
source activate /projects/a9009/sbc538/documentation/documentation-env
pip install django-ckeditor
```
