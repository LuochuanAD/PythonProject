from vizro import Vizro
import vizro.models as vm
import vizro.plotly.express as px
from vizro.actions import export_data
from vizro.actions import filter_interaction
from vizro.tables import dash_ag_grid
home_page = vm.Page(
    title="Home Page",
    components=[
        vm.Card(
            text="""
                    ![](assets/images/icons/content/collections.svg#icon-top)

                    ### First Page

                    Exemplary first dashboard page.
                    """,
            href="/first-page",
        ),
        vm.Card(
            text="""
                    ![](assets/images/icons/content/features.svg#icon-top)

                    ### Second Page

                    Exemplary second dashboard page.
                    """,
            href="/second-page",
        ),
    ],

)
iris_data = px.data.iris()
df = px.data.gapminder()
gapminder_data = (
        df.groupby(by=["continent", "year"]).
            agg({"lifeExp": "mean", "pop": "sum", "gdpPercap": "mean"}).reset_index()
    )

first_page = vm.Page(
    title="First Page",
    layout=vm.Layout(grid=[[0,0],[1,2],[1,2],[1,2]]),
    components=[
        vm.Card(
            text="""
        # 标题
        内容......
            """,
        ),
        vm.Graph(
            id="box",
            figure=px.box(gapminder_data, x="continent", y="lifeExp", color="continent",
                            labels={"lifeExp": "Life Expectancy", "continent":"Continent"},title='箱子图'),
        ),
        vm.Graph(
            id="line",
            figure=px.line(gapminder_data, x="year", y="pop", color="continent",
                    labels={"year": "Year", "continent": "Continent",
                    "pop":"GDP Per Capxxx"}, title='折线图'),
        ),


    ],
    controls=[vm.Filter(column="continent", targets=["box", "line"]),],
)

second_page = vm.Page(
    title="Second Page",
    components=[
        vm.Graph(
            id="scatter_iris",
            figure=px.scatter(iris_data, x="sepal_width", y="sepal_length", color="species",
                color_discrete_map={"setosa": "#00b4ff", "versicolor": "#ff9222"},
                labels={"sepal_width": "Sepal Width", "sepal_length": "Sepal Length",
                        "species": "Species"},title='点状图',
            ),
        ),
        vm.Graph(
            id="hist_iris",
            figure=px.histogram(iris_data, x="sepal_width", color="species",
                color_discrete_map={"setosa": "#00b4ff", "versicolor": "#ff9222"},
                labels={"sepal_width": "Sepal Width", "count": "Count",
                        "species": "Species"},title='柱状图',
            ),
        ),
    ],
    controls=[
        vm.Parameter(
            targets=["scatter_iris.color_discrete_map.virginica",
                        "hist_iris.color_discrete_map.virginica"],
            selector=vm.Dropdown(
                options=["#ff5267", "#3949ab"], multi=False, value="#3949ab", title="Color Virginica"),
            ),
        vm.Parameter(
            targets=["scatter_iris.opacity"],
            selector=vm.Slider(min=0, max=1, value=0.8, title="Opacity"),
        ),
    ],
)
iris = px.data.iris()

third_page = vm.Page(
    title="Using actions",
    components=[
        vm.Graph(
            id="scatter",
            figure=px.scatter(iris, x="petal_length", y="sepal_length", color="sepal_width"),
        ),
        vm.Graph(
            id="hist",
            figure=px.histogram(iris, x="petal_length", color="species"),
        ),
        vm.Button(
            text="Export data",
            actions=[
                vm.Action(
                    function=export_data(
                        targets=["scatter"],
                    )
                ),
                vm.Action(
                    function=export_data(
                        targets=["hist"],
                        file_format="csv",
                    )
                ),
            ],
        ),
    ],
    controls=[
        vm.Filter(column="species"),
    ],
)
df_gapminder = px.data.gapminder().query("year == 2007")
fourth_page = vm.Page(
            title="Filter interaction",
            components=[
                vm.AgGrid(
                    figure=dash_ag_grid(data_frame=df_gapminder),
                    actions=[
                        vm.Action(function=filter_interaction(targets=["scatter_relation_2007"]))
                    ],
                ),
                vm.Graph(
                    figure=px.box(
                        df_gapminder,
                        x="continent",
                        y="lifeExp",
                        color="continent",
                        custom_data=["continent"],
                    ),
                    actions=[vm.Action(function=filter_interaction(targets=["scatter_relation_2007"]))],
                ),
                vm.Graph(
                    id="scatter_relation_2007",
                    figure=px.scatter(
                        df_gapminder,
                        x="gdpPercap",
                        y="lifeExp",
                        size="pop",
                        color="continent",
                    ),
                ),
            ],
            controls=[vm.Filter(column='continent')]
)

dashboard = vm.Dashboard(pages=[home_page,first_page,second_page,third_page,fourth_page])
Vizro().build(dashboard).run(debug=True)