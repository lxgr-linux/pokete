package msg

type EmptyMsg struct {
    BaseMsg
}

func (e EmptyMsg) GetType() Type {
    return "internal.empty"
}

func NewEmptyMsg() EmptyMsg {
    return EmptyMsg{BaseMsg{}}
}
