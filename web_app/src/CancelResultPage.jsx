import { Result,Typography } from 'antd';
const { Text } = Typography;

export default function ResultPage(props) {
    return (
        <Result
            title="你已取消自动签到"
            subTitle="如果你需要重新使用，请回到注册页面重新注册。"
            extra={[
                <Text>分享给朋友：<Text copyable>https://serene.net.cn</Text></Text>
            ]}
        />
    );
}