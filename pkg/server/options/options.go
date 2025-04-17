package options

type Func func(*Options) error

func WithGreeting(greeting string) Func {
	return func(o *Options) error {
		o.GreetingText = greeting
		return nil
	}
}

type Options struct {
	GreetingText string
}

func FromOptionFuncs(opts ...Func) (*Options, error) {
	o := Options{}
	for _, fun := range opts {
		err := fun(&o)
		if err != nil {
			return nil, err
		}
	}
	return &o, nil
}
