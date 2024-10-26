import Cookies from "js-cookie";
import { useState } from "react";
import "./App.css";

function App() {
  const [tokenData, setTokenData] = useState(null); // トークンデータを保存するための状態
  const [message, setMessage] = useState(null); // メッセージを保存するための状態
  const [error, setError] = useState<string | null>(null); // エラーメッセージを保存するための状態
  const handleValidToken = async () => {
    try {
      const response = await fetch("http://localhost/api/token/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${Cookies.get("AUTH_TOKEN")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      // 必要なデータだけを抽出
      const extractedData = {
        name: data.name,
        email: data.email,
        preferred_username: data.preferred_username,
        roles: data.realm_access.roles,
        resource_access: data.resource_access,
      };

      console.log("Login successful, tokens saved in cookies");
      setTokenData(extractedData);
    } catch (error) {
      setError(error.message);
    }
  };
  const handleRefreshToken = async () => {
    try {
      setTokenData(null);
      const response = await fetch("http://localhost/api/token/refresh", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${Cookies.get("AUTH_REF_TOKEN")}`,
        },
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
    } catch (error) {
      setError(error.message);
    }
  };
  const handleRequest = async () => {
    try {
      const response = await fetch("http://localhost/api/response", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${Cookies.get("AUTH_TOKEN")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();

      setMessage(data);
    } catch (error) {
      setError(error.message);
    }
  };
  return (
    <>
      <div className="card">
        {/* エラーメッセージを表示 */}
        {error && (
          <div className="error-popup">
            <p>{error}</p>
            <button onClick={() => setError(null)}>Close</button>
          </div>
        )}
        <button
          onClick={() => {
            window.location.href = "http://localhost/api/login";
            setTokenData(null);
          }}
        >
          Submit to Login
        </button>
        <br />
        <br />
        <br />
        <button onClick={handleRefreshToken}>Submit to Token Refresh</button>
        <br />
        <br />
        <br />
        <button onClick={handleValidToken}>Submit to Valid Token</button>
        {tokenData && (
          <div>
            <h3>Token Data</h3>
            <div className="token-data">
              <p>
                <strong>名前:</strong> {tokenData.name}
              </p>
              <p>
                <strong>メールアドレス:</strong> {tokenData.email}
              </p>
              <p>
                <strong>Preferred Username:</strong>{" "}
                {tokenData.preferred_username}
              </p>
              <p>
                <strong>ロール:</strong> {tokenData.roles.join(", ")}
              </p>
              <br />
              <div style={{ textAlign: "left" }}>
                <strong>リソースアクセス</strong>
                <ul>
                  {Object.entries(tokenData.resource_access).map(
                    ([key, value]) => (
                      <li key={key}>
                        {key}: {value.roles.join(", ")}
                      </li>
                    )
                  )}
                </ul>
              </div>
            </div>
          </div>
        )}
        <br />
        <br />
        <br />
        <button onClick={handleRequest}>Submit to Request</button>
        {message && (
          <div>
            <h3>Response</h3>
            <div className="token-data">
              <p>
                <strong>メッセージ:</strong> {message.message}
              </p>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
