const path = require("path");
module.exports = ({ config }) => {
  config.module.rules.push({
    test: /\.(ts|tsx)$/,
    use: [
      {
        loader: require.resolve("react-docgen-typescript-loader"),
      },
      {
        loader: require.resolve("@storybook/addon-storysource/loader"),
        options: { parser: "typescript" },
      },
      {
        loader: require.resolve("ts-loader"),
        options: {
          transpileOnly: true,
        },
      },
    ],
  });
  config.resolve.extensions.push(".js", ".jsx", ".ts", ".tsx");
  return config;
};
