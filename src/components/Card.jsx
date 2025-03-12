import { motion } from 'framer-motion';

const Card = ({ title, content, image, ...props }) => {
  return (
    <motion.div
      className="card"
      whileHover={{ 
        y: -10, 
        boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
      }}
      transition={{ duration: 0.3 }}
      {...props}
    >
      {image && (
        <div className="card-image">
          <img src={image} alt={title} />
        </div>
      )}
      <div className="card-content">
        <h3>{title}</h3>
        <p>{content}</p>
      </div>
    </motion.div>
  );
};

export default Card; 