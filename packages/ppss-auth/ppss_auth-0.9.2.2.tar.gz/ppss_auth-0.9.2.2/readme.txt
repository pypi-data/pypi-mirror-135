** To create a new ppss_auth db revision:
cd ppss_auth/alembic
alembic -c alembic.ini revision --autogenerate -m "your comment here"


** babel/i18n
requires
apt install gettext
pip install babel

#extract strings from py, jinja2, mako
pybabel extract -F babel.ini -o ${project}/locale/${project}.pot ${project} 
#pybabel extract -F babel.ini -k _t:2 -o ${project}/locale/${project}.pot ${project} 

#first time creation
mkdir -p ${project}/${lang}/LC_MESSAGES
msginit -l ${lang} -o ${project}/locale/${lang}/LC_MESSAGES/${project}.po --input ${project}/locale/${project}.pot

#update
msgmerge --update ${project}/locale/${lang}/LC_MESSAGES/${project}.po ${project}/locale/${project}.pot

#compile .po into .mo
msgfmt -o ${project}/locale/${lang}/LC_MESSAGES/${project}.mo ${project}/locale/${lang}/LC_MESSAGES/${project}.po

