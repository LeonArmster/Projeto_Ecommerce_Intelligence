COPY raw.{table_name}
FROM '{file_path}'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER '|'
);