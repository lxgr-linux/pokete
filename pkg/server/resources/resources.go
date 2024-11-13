package resources

import (
	"encoding/json"
	"os"
	"path"

	"github.com/lxgr-linux/pokete/resources"
)

type Resources struct {
	Assets     resources.Assets
	BaseAssets resources.BaseAssets
}

func FromDir(baseDir string) (*Resources, error) {
	assets, err := readFile[resources.Assets](path.Join(baseDir, "assets.json"))
	if err != nil {
		return nil, err
	}

	baseAssets, err := readFile[resources.BaseAssets](path.Join(baseDir, "base_assets.json"))
	if err != nil {
		return nil, err
	}

	return &Resources{assets, baseAssets}, nil
}

func FromBytes(assetBytes []byte, baseAssetBytes []byte) (*Resources, error) {
	assets, err := readBytes[resources.Assets](assetBytes)
	if err != nil {
		return nil, err
	}

	baseAssets, err := readBytes[resources.BaseAssets](baseAssetBytes)
	if err != nil {
		return nil, err
	}

	return &Resources{assets, baseAssets}, nil
}

func readFile[T any](fileName string) (temp T, err error) {
	content, err := os.ReadFile(fileName)
	if err != nil {
		return
	}

	err = json.Unmarshal(content, &temp)

	return
}

func readBytes[T any](b []byte) (temp T, err error) {
	err = json.Unmarshal(b, &temp)
	return
}
