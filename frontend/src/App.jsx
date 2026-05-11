import "./App.css";
import { useState } from "react";

export default function App() {
  const [numbers, setNumbers] = useState([]);
  const [loading, setLoading] = useState(false);

  const reset = () => {
    setNumbers([]);
  };

  const pickNumbers = async () => {
    setLoading(true);

    try {
      const res = await fetch("https://lotto-web-5eqz.onrender.com/pick");
      const data = await res.json();

      console.log("받은 데이터:", data);

      setNumbers(Array.isArray(data.numbers) ? data.numbers : []);
    } catch (err) {
      console.error(err);
      alert("서버 연결 실패! 백엔드가 켜져 있는지 확인해줘.");
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="card">
        <h1>로또 번호 추천기</h1>

        <p className="desc">
          랜덤으로 로또 번호 추천
        </p>

        <div className="actions">
          <button onClick={pickNumbers} disabled={loading} className="btn primary">
            {loading
              ? "번호 생성 중..."
              : numbers.length > 0
                ? "새로 뽑기"
                : "5게임 뽑기"}
          </button>

          {numbers.length > 0 && (
            <button onClick={reset} disabled={loading} className="btn secondary">
              뒤로(처음으로)
            </button>
          )}
        </div>

        <div className="results">
          {numbers.map((game, idx) => (
            <div className="game" key={idx}>
              <h3>{idx + 1}게임</h3>

              <div className="balls">
                {(Array.isArray(game) ? game : []).map((num) => (
                  <div className="ball" key={num}>
                    {num}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}