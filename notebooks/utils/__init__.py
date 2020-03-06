import altair as alt

def interactive_chart(df):
    nearest = alt.selection(
        type='single',
        nearest=True,
        on='mouseover',
        fields=['week'],
        empty='none'
    )

    line = (
        alt.Chart(df)
        .mark_line(interpolate='basis')
        .encode(
            x='week',
            y='read',
            color='year:O'
        )
    )

    selectors = (
        alt.Chart(df)
        .mark_point()
        .encode(
            x='week',
            opacity=alt.value(0)
        )
        .add_selection(nearest)
    )

    points = (
        line
        .mark_point()
        .encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
    )

    text = (
        line
        .mark_text(align='left', dx=5, dy=-5)
        .encode(
            text=alt.condition(nearest, 'read', alt.value(' '))
        )
    )

    rules = (
        alt.Chart(df)
        .mark_rule(color='red')
        .encode(x='week')
        .transform_filter(nearest)
    )

    chart = (
        alt.layer(line, selectors, points, rules, text)
        .properties(
            width=500,
            height=300,
            background='white',
            title='goodreads Challenge'
        )
    )

    return chart
