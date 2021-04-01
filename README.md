# Install
```
module purge all
module load python/anaconda3.6
conda create --prefix /projects/a9009/sbc538/documentation/documentation-env -c conda-forge django-extensions django python=3.8
source activate /projects/a9009/sbc538/documentation/documentation-env
pip install django-ckeditor
```

# Run launch server
```
./manage.py runserver
```

# Use curl
Make sure this is done on the same node that you ran the server on.
```
curl http://127.0.0.1:8000/ -o software.html
```

# For populating spack module
```
 . /projects/a9009/sbc538/spack/spack/share/spack/setup-env.sh
```
