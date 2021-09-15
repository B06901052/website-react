import React from "react";
import { makeStyles, ThemeProvider, useTheme } from "@material-ui/core/styles";
import { Box, Typography } from "@material-ui/core";
import SyntaxHighlighter from 'react-syntax-highlighter';
import { atomOneDarkReasonable } from 'react-syntax-highlighter/dist/esm/styles/hljs';

import { Section } from "./components/Sections";
import { Title } from "./components/Titles";
import { capitalizeFirstLetter, Strong } from "./components/Utilies";
import { subscribe_link } from "./Data";

const code = '\
print("Hello world!")\n\
for x in range(10):\n\
    print("Hello world!")\
'

// const markdown = (
//     <MarkDownElement>
//         #test
//     </MarkDownElement>
// )

const news = [
    {
        title: "This is a code block",
        date: new Date(2021, 9, 15),
        content: (
            <SyntaxHighlighter language="python" style={atomOneDarkReasonable} showLineNumbers="ture" align="left">
                {code}
            </SyntaxHighlighter>
        ),
    },
    // {
    //     title: "This is a markdown block",
    //     date: new Date(2021, 9, 15),
    //     content: (
    //         markdown
    //     ),
    // },
    {
        title: "This is another title",
        date: new Date(2021, 9, 13),//y,m,d,h,m,s,ms
        content: (
            <span>
                just a test for long content.<br /><br />
                臣亮言：先帝創業未半而中道崩殂，今天下三分，益州疲敝，此誠危急存亡之秋也。然侍衞之臣不懈於內，忠志之士忘身於外者，蓋追先帝之殊遇，欲報之於陛下也。
                <br /><br />
                誠宜開張聖聽，以光先帝遺德，恢弘志士之氣，不宜妄自菲薄，引喻失義，以塞忠諫之路也。
                <br /><br />
                宮中府中，俱爲一體，陟罰臧否，不宜異同。若有作奸犯科及爲忠善者，宜付有司論其刑賞，以昭陛下平明之治，不宜偏私，使內外異法也。
                <br /><br />
                侍中、侍郎郭攸之、費禕、董允等，此皆良實，志慮忠純，是以先帝簡拔以遺陛下。愚以爲宮中之事，事無大小，悉以咨之，然後施行，必能裨補闕漏，有所廣益。
                <br /><br />
                將軍向寵，性行淑均，曉暢軍事，試用之於昔日，先帝稱之曰能，是以衆議舉寵爲督。愚以爲營中之事，悉以咨之，必能使行陣和睦，優劣得所也。
                <br /><br />
                親賢臣，遠小人，此先漢所以興隆也；親小人，遠賢臣，此後漢所以傾頹也。先帝在時，每與臣論此事，未嘗不歎息痛恨於桓、靈也。侍中、尚書、長史、參軍，此悉貞亮死節之臣也，願陛下親之信之，則漢室之隆，可計日而待也。
                <br /><br />
                臣本布衣，躬耕於南陽，苟全性命於亂世，不求聞達於諸侯。先帝不以臣卑鄙，猥自枉屈，三顧臣於草廬之中，諮臣以當世之事，由是感激，遂許先帝以驅馳。後值傾覆，受任於敗軍之際，奉命於危難之間，爾來二十有一年矣。先帝知臣謹慎，故臨崩寄臣以大事也。受命以來，夙夜憂歎，恐託付不效，以傷先帝之明，故五月渡瀘，深入不毛。今南方已定，兵甲已足，當獎率三軍，北定中原，庶竭駑鈍，攘除姦凶，興復漢室，還于舊都，此臣所以報先帝，而忠陛下之職分也。至於斟酌損益，進盡忠言，則攸之、禕、允之任也。
                <br /><br />
                願陛下託臣以討賊興復之效；不效，則治臣之罪，以告先帝之靈。若無興德之言，則責攸之、禕、允等之慢，以彰其咎。陛下亦宜自謀，以諮諏善道，察納雅言。深追先帝遺詔，臣不勝受恩感激。
            </span>),
    },
    {
        title: "This is a title",
        date: new Date(2021, 9, 12),//y,m,d,h,m,s,ms
        content: (
            <span>
                just a test for short content.
            </span>),
    },
    // {
    //     title: "This is a title",
    //     date: new Date(yyyy, m, d),
    //     content: (
    //         <span>
    //             Your content
    //         </span>),
    // },
]

const useStyles = makeStyles((theme) => ({
    taskName: {
        fontWeight: "bold",
        marginBottom: theme.spacing(2),
    },
}));

function Post(props) {
    return (
        <ThemeProvider>
            <Box maxWidth={800} margin="auto">
                <Section>
                    <Title
                        title={capitalizeFirstLetter(
                            props.title.toLowerCase()
                        )}
                        titleVariant="h5"
                        divider={true}
                        color="textPrimary"
                    />
                    <Typography
                        variant="body1"
                        color="textSecondary"
                        align="right"
                        style={{ fontSize: 10 }}
                    >
                        {props.date.toDateString()}
                    </Typography>
                    <Typography
                        variant="body1"
                        color="textSecondary"
                    >
                        {props.content}
                    </Typography>

                </Section>
            </Box>
        </ThemeProvider >
    )
}

function News(props) {
    const classes = useStyles();
    const theme = useTheme();

    return (
        <React.Fragment>
            <Section margin={theme.spacing(8, "auto", 1)}>
                <Title
                    title="News"
                    description={
                        <span><Strong><a href={subscribe_link} target="_blank" rel="noopener noreferrer">Subscribe</a></Strong> our enews to receive all the latest information about SUPERB.</span>
                    }
                />
            </Section>
            {news.map(Post)}

        </React.Fragment >
    );
}

export default News;