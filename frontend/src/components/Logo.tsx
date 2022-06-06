interface LogoProps {
  bg: boolean;
  size?: number;
}

const Logo = (props: LogoProps) => {
  let size = props.size;
  if (!size) size = 36;

  return (
    <>
      {props.bg ? (
        <svg
          width={size}
          height={size}
          viewBox="0 0 114 114"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <rect width="114" height="114" rx="20" fill="white" />
          <rect width="114" height="114" rx="20" fill="#202124" />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M18.1137 60.531C16.161 58.5784 16.161 55.4126 18.1137 53.46L35.7913 35.7823L48.5192 48.5102L41.4578 55.5717C40.6689 56.3605 40.6689 57.6395 41.4578 58.4283L48.5147 65.4853L35.7913 78.2087L18.1137 60.531Z"
            fill="url(#paint0_linear_3_8)"
          />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M53.4645 18.1091C55.4171 16.1565 58.5829 16.1565 60.5355 18.1091L78.2132 35.7868L65.4853 48.5147L58.4238 41.4532C57.635 40.6644 56.356 40.6644 55.5672 41.4532L48.5102 48.5102L35.7868 35.7868L53.4645 18.1091Z"
            fill="url(#paint1_linear_3_8)"
          />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M95.8909 53.4645C97.8435 55.4171 97.8435 58.5829 95.8909 60.5355L78.2132 78.2132L65.4853 65.4853L72.5468 58.4238C73.3356 57.635 73.3356 56.356 72.5468 55.5672L65.4898 48.5102L78.2132 35.7868L95.8909 53.4645Z"
            fill="url(#paint2_linear_3_8)"
          />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M60.5355 95.8909C58.5829 97.8435 55.4171 97.8435 53.4645 95.8909L35.7868 78.2132L48.5147 65.4853L55.5762 72.5468C56.365 73.3356 57.644 73.3356 58.4328 72.5468L65.4898 65.4898L78.2132 78.2132L60.5355 95.8909Z"
            fill="url(#paint3_linear_3_8)"
          />
          <defs>
            <linearGradient
              id="paint0_linear_3_8"
              x1="35.5781"
              y1="35.5691"
              x2="57.0781"
              y2="57.0691"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
            <linearGradient
              id="paint1_linear_3_8"
              x1="78.4264"
              y1="35.5736"
              x2="56.9264"
              y2="57.0736"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
            <linearGradient
              id="paint2_linear_3_8"
              x1="78.4264"
              y1="78.4264"
              x2="56.9264"
              y2="56.9264"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
            <linearGradient
              id="paint3_linear_3_8"
              x1="35.5736"
              y1="78.4264"
              x2="57.0736"
              y2="56.9264"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
          </defs>
        </svg>
      ) : (
        <svg
          width={size}
          height={size}
          viewBox="0 0 85 85"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M3.54005 45.9574C1.58743 44.0048 1.58743 40.839 3.54005 38.8864L21.2177 21.2087L33.9456 33.9366L26.8842 40.9981C26.0953 41.7869 26.0953 43.0659 26.8842 43.8547L33.9411 50.9117L21.2177 63.6351L3.54005 45.9574Z"
            fill="url(#paint0_linear_3_86)"
          />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M38.8909 3.53553C40.8435 1.58291 44.0093 1.58291 45.9619 3.53553L63.6396 21.2132L50.9117 33.9411L43.8502 26.8796C43.0614 26.0908 41.7824 26.0908 40.9936 26.8796L33.9366 33.9366L21.2132 21.2132L38.8909 3.53553Z"
            fill="url(#paint1_linear_3_86)"
          />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M81.3173 38.8909C83.2699 40.8435 83.2699 44.0093 81.3173 45.9619L63.6396 63.6396L50.9117 50.9117L57.9732 43.8502C58.762 43.0614 58.762 41.7824 57.9732 40.9936L50.9162 33.9366L63.6396 21.2132L81.3173 38.8909Z"
            fill="url(#paint2_linear_3_86)"
          />
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M45.9619 81.3173C44.0093 83.2699 40.8435 83.2699 38.8909 81.3173L21.2132 63.6396L33.9411 50.9117L41.0026 57.9732C41.7914 58.762 43.0704 58.762 43.8592 57.9732L50.9162 50.9162L63.6396 63.6396L45.9619 81.3173Z"
            fill="url(#paint3_linear_3_86)"
          />
          <defs>
            <linearGradient
              id="paint0_linear_3_86"
              x1="21.0045"
              y1="20.9955"
              x2="42.5045"
              y2="42.4955"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
            <linearGradient
              id="paint1_linear_3_86"
              x1="63.8528"
              y1="21"
              x2="42.3528"
              y2="42.5"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
            <linearGradient
              id="paint2_linear_3_86"
              x1="63.8528"
              y1="63.8528"
              x2="42.3528"
              y2="42.3528"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
            <linearGradient
              id="paint3_linear_3_86"
              x1="21"
              y1="63.8528"
              x2="42.5"
              y2="42.3528"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#DBDBDB" stopOpacity="0.8" />
              <stop offset="1" stopColor="#DBDBDB" />
            </linearGradient>
          </defs>
        </svg>
      )}
    </>
  );
};

export default Logo;
