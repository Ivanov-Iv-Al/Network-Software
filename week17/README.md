## CI пайплайн (GitHub Actions)

Файл `.github/workflows/ci.yml` (концептуально) выполняет:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint-and-test:
    strategy:
      matrix:
        service: [api-gateway, task-service, notification-service]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      - name: Lint proto
        run: buf lint proto/
      - name: Unit tests
        run: cd ${{ matrix.service }} && go test ./...
      - name: Build Docker image
        run: docker build -t ${{ matrix.service }} ./${{ matrix.service }}
      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USER }} --password-stdin
          docker tag ${{ matrix.service }} yourrepo/${{ matrix.service }}:latest
          docker push yourrepo/${{ matrix.service }}:latest