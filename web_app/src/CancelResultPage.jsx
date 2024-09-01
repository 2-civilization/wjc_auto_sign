import { Result,Typography } from 'antd';
const { Text } = Typography;

export default function ResultPage(props) {
    return (
        <Result
            title="你已取消自动签到"
            subTitle="如果你需要重新使用，请回到注册页面重新注册。"
            extra={[
                <>
                <p>分享给朋友：<Text copyable>https://serene.net.cn</Text></p>
                <p>开源地址：</p>
                <p>
                    <a href='https://gitee.com/saucer216/wjc_auto_sign'><img src='https://gitee.com/saucer216/wjc_auto_sign/widgets/widget_5.svg?color=red' alt='Fork me on Gitee'></img></a>
                    <a href='https://github.com/sz134055/wjc_auto_sign'><img src='https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png' width='50px' height='50px' alt='Fork me on GitHub'></img></a>
                </p>
                </>
            ]}
        />
    );
}