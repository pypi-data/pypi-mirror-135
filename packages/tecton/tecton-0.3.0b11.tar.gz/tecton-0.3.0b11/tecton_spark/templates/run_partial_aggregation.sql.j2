{%- set join_key_list = join_keys|join(", ")  %}

SELECT
    {{ join_key_list }},
    {%- for column, functions in aggregations.items() -%}
        {%- for function, snowflake_function in functions %}
            {{ function }}_{{ column }} AS {{ column }}_{{ function }}_{{ slide_interval_string }},
        {%- endfor %}
    {%- endfor %}
    {{ timestamp_key }} AS TILE_START_TIME,
    TO_TIMESTAMP(DATE_PART(EPOCH_SECOND, {{ timestamp_key }}) + {{ slide_interval.ToSeconds() }}) AS TILE_END_TIME
FROM (
    {{ source }}
)
