import { Result,Typography } from 'antd';
const { Text } = Typography;

export default function ResultPage(props) {
    return (
        <Result
            status="success"
            title="完成自动签到注册！"
            subTitle="你已完成自动签到注册，自动签到脚本将会在每晚20:30开始为你自动签到并发送结果通知邮件，超过长时间未收到通知邮件请反馈并手动签到。"
            extra={[
                <Text>分享给朋友：<Text copyable>https://serene.com.cn</Text></Text>
            ]}
        />
    );
}