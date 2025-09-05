import requests  # type: ignore[import-untyped]
import semantic_kernel
import googleapiclient
import google.auth
import google_auth_oauthlib


def main() -> None:
    print("Hello, World!")
    print(f"requests version: {requests.__version__}")
    print(f"semantic-kernel version: {semantic_kernel.__version__}")
    print(f"google-api-python-client version: {googleapiclient.__version__}")
    print(f"google-auth version: {google.auth.__version__}")
    print(f"google-auth-oauthlib version: {google_auth_oauthlib.__version__}")


if __name__ == "__main__":
    main()
