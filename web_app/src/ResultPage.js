import { Result,Typography } from 'antd';
const { Text } = Typography;

export default function ResultPage(props) {
    return (
        <Result
            status="success"
            title="完成自动签到注册！"
            subTitle="你已完成自动签到注册，自动签到脚本将会在每晚20:30开始为你自动签到，并会在签到失败时向你发送邮件提醒。"
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