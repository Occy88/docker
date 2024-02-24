FROM octo_base
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--access-logfile", "-", "--workers", "4", "--bind", ":8000"]
