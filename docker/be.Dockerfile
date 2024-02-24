
FROM octo_base AS final
COPY --from=octo_base_python /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
CMD ["python -m", "uvicorn", "web.main:app", "--reload", "--host", "0.0.0.0", "--port","8000"]